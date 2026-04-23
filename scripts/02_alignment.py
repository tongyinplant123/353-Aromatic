#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Multiple Sequence Alignment Script for 353 Phylogenomics Pipeline
Handles alignment with MAFFT/MUSCLE and trimming with TrimAl
"""

import os
import sys
import argparse
import yaml
import subprocess
from pathlib import Path
from tqdm import tqdm


def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def run_alignment(seq_file, output_file, tool, algorithm):
    """Run multiple sequence alignment"""
    seq_file = str(seq_file)
    output_file = str(output_file)
    
    if tool == 'mafft':
        cmd = [
            'mafft',
            '--' + algorithm,
            seq_file
        ]
    elif tool == 'muscle':
        cmd = [
            'muscle',
            '-align', seq_file,
            '-output', output_file
        ]
    else:
        raise ValueError(f"Unknown alignment tool: {tool}")
    
    try:
        with open(output_file, 'w') as out:
            result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, 
                                  text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running alignment: {e.stderr}")
        return False


def run_trimming(aligned_file, output_file, tool, method):
    """Run alignment trimming"""
    aligned_file = str(aligned_file)
    output_file = str(output_file)
    
    if tool == 'trimal':
        cmd = [
            'trimal',
            '-in', aligned_file,
            '-out', output_file,
            '-' + method
        ]
    else:
        raise ValueError(f"Unknown trimming tool: {tool}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running trimming: {e.stderr}")
        return False


def process_gene_alignment(gene_name, config, input_dir, output_dir):
    """Process alignment for a single gene"""
    gene_input_dir = input_dir / gene_name
    gene_output_dir = output_dir / gene_name
    gene_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Input and output files
    input_file = gene_input_dir / 'processed.fasta'
    aligned_file = gene_output_dir / 'aligned.fasta'
    trimmed_file = gene_output_dir / 'aligned_trimmed.fasta'
    
    if not input_file.exists():
        print(f"Warning: Input file not found for {gene_name}: {input_file}")
        return False
    
    # Run alignment
    alignment_config = config['alignment']
    success = run_alignment(
        input_file, 
        aligned_file,
        alignment_config['tool'],
        alignment_config['algorithm']
    )
    
    if not success:
        print(f"Error: Alignment failed for {gene_name}")
        return False
    
    # Run trimming if enabled
    if alignment_config['trim']:
        success = run_trimming(
            aligned_file,
            trimmed_file,
            alignment_config['trim_tool'],
            alignment_config['trim_method']
        )
        
        if not success:
            print(f"Error: Trimming failed for {gene_name}")
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Multiple sequence alignment for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--input-dir', default='results/preprocessing/sequences', help='Input directory')
    parser.add_argument('--output-dir', default='results/alignments', help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directories
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get list of genes to process
    genes = [d.name for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(genes)} genes to process")
    
    # Process each gene
    success_count = 0
    fail_count = 0
    
    for gene in tqdm(genes, desc='Aligning genes'):
        success = process_gene_alignment(gene, config, input_dir, output_dir)
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\nAlignment complete!")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Results saved to: {output_dir}")


if __name__ == '__main__':
    main()
