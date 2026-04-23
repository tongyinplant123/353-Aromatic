#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Concatenation Analysis Script for 353 Phylogenomics Pipeline
Handles supermatrix construction and ML analysis with IQ-TREE/RAxML-NG
"""

import os
import sys
import argparse
import yaml
import subprocess
from pathlib import Path
from Bio import SeqIO
from tqdm import tqdm


def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def read_alignment(alignment_file):
    """Read alignment file and return sequences"""
    sequences = {}
    for record in SeqIO.parse(alignment_file, 'fasta'):
        sequences[record.id] = str(record.seq)
    return sequences


def build_supermatrix(gene_dirs, config):
    """Build supermatrix from individual gene alignments"""
    all_species = set()
    gene_data = {}
    
    for gene_dir in tqdm(gene_dirs, desc='Reading gene alignments'):
        gene_name = gene_dir.name
        
        # Try trimmed alignment first, then aligned
        alignment_file = gene_dir / 'aligned_trimmed.fasta'
        if not alignment_file.exists():
            alignment_file = gene_dir / 'aligned.fasta'
        
        if not alignment_file.exists():
            print(f"Warning: Alignment not found for {gene_name}")
            continue
        
        sequences = read_alignment(alignment_file)
        gene_data[gene_name] = sequences
        
        # Collect all species
        for species in sequences.keys():
            all_species.add(species)
    
    # Determine alignment length for each gene
    gene_lengths = {}
    for gene_name, sequences in gene_data.items():
        if sequences:
            gene_lengths[gene_name] = len(list(sequences.values())[0])
        else:
            gene_lengths[gene_name] = 0
    
    # Build supermatrix
    supermatrix = {}
    for species in all_species:
        supermatrix[species] = {}
        for gene_name in gene_data.keys():
            if species in gene_data[gene_name]:
                supermatrix[species][gene_name] = gene_data[gene_name][species]
            else:
                # Missing data as gaps
                supermatrix[species][gene_name] = '-' * gene_lengths[gene_name]
    
    return supermatrix, list(gene_data.keys()), gene_lengths


def write_phylip_format(supermatrix, gene_names, output_file):
    """Write supermatrix in PHYLIP format"""
    species_list = list(supermatrix.keys())
    num_species = len(species_list)
    total_length = sum(len(supermatrix[species][gene]) for species in species_list[:1] for gene in gene_names)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f" {num_species} {total_length}\n")
        
        for species in species_list:
            sequence = ''.join(supermatrix[species][gene] for gene in gene_names)
            f.write(f"{species[:10]:<10} {sequence}\n")


def write_partition_file(gene_names, gene_lengths, output_file):
    """Write partition file for IQ-TREE"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Partition file for IQ-TREE\n")
        
        start = 1
        for i, gene_name in enumerate(gene_names):
            length = gene_lengths[gene_name]
            end = start + length - 1
            f.write(f"DNA, {gene_name} = {start}-{end}\n")
            start = end + 1


def run_concatenation_analysis(supermatrix_file, partition_file, output_dir, config):
    """Run concatenation analysis with IQ-TREE"""
    output_dir = str(output_dir)
    
    analysis_config = config['concatenation']['analysis']
    tool = analysis_config.get('tool', 'iqtree')
    
    if tool == 'iqtree':
        cmd = [
            'iqtree2',
            '-s', supermatrix_file,
            '-p', partition_file,
            '-m', analysis_config['model'],
            '-B', str(analysis_config['bootstrap']),
            '-bnni',
            '-pre', str(Path(output_dir) / 'supermatrix'),
            '-T', str(analysis_config['threads']),
            '-nt', 'AUTO'
        ]
        
        if analysis_config.get('sh_alrt', True):
            cmd.insert(-2, '-alrt')
            cmd.insert(-2, str(analysis_config.get('bootstrap', 1000)))
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=output_dir)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running IQ-TREE: {e.stderr}")
            return False
    
    elif tool == 'raxml-ng':
        cmd = [
            'raxml-ng',
            '--msa', supermatrix_file,
            '--model', 'GTR+G',
            '--threads', str(analysis_config['threads']),
            '--prefix', str(Path(output_dir) / 'supermatrix'),
            '--bs-trees', str(analysis_config['bootstrap'])
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running RAxML-NG: {e.stderr}")
            return False
    
    else:
        print(f"Error: Unknown tool: {tool}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Concatenation analysis for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--input-dir', default='results/alignments', help='Input directory')
    parser.add_argument('--output-dir', default='results/concatenation', help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directories
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get list of gene directories
    gene_dirs = [d for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(gene_dirs)} genes")
    
    # Build supermatrix
    supermatrix, gene_names, gene_lengths = build_supermatrix(gene_dirs, config)
    
    print(f"Built supermatrix with {len(supermatrix)} species and {len(gene_names)} genes")
    
    # Write supermatrix in PHYLIP format
    supermatrix_file = output_dir / 'supermatrix.phylip'
    write_phylip_format(supermatrix, gene_names, supermatrix_file)
    
    # Write partition file
    partition_file = output_dir / 'partitions.nex'
    write_partition_file(gene_names, gene_lengths, partition_file)
    
    # Run concatenation analysis
    print("Running concatenation analysis...")
    success = run_concatenation_analysis(supermatrix_file, partition_file, output_dir, config)
    
    if success:
        print(f"\nConcatenation analysis complete!")
        print(f"Results saved to: {output_dir}")
        
        # Show tree file location
        tree_file = output_dir / 'supermatrix.treefile'
        if tree_file.exists():
            print(f"Final tree: {tree_file}")
    else:
        print("Error: Concatenation analysis failed")


if __name__ == '__main__':
    main()
