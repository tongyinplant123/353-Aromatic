#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gene Tree Inference Script for 353 Phylogenomics Pipeline
Handles gene tree inference with IQ-TREE or RAxML-NG
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


def infer_gene_tree_iqtree(aligned_file, output_dir, config):
    """Infer gene tree using IQ-TREE"""
    aligned_file = str(aligned_file)
    output_dir = str(output_dir)
    
    model_config = config['gene_tree']
    
    cmd = [
        'iqtree2',  # or 'iqtree' depending on installation
        '-s', aligned_file,
        '-m', model_config['model_selection'],
        '-B', str(model_config['bootstrap_replicates']),
        '-bnni',  # Best-NNI for UFBoot
        '-pre', str(Path(output_dir) / 'gene_tree'),
        '-T', str(model_config['threads']),
        '-nt', 'AUTO'  # Use automatic thread allocation
    ]
    
    if model_config['ufboot_replicates'] > 0:
        cmd.extend(['-bnni'])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=output_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running IQ-TREE: {e.stderr}")
        return False


def infer_gene_tree_raxml(aligned_file, output_dir, config):
    """Infer gene tree using RAxML-NG"""
    aligned_file = str(aligned_file)
    output_prefix = str(Path(output_dir) / 'gene_tree')
    
    model_config = config['gene_tree']
    
    cmd = [
        'raxml-ng',
        '--msa', aligned_file,
        '--model', model_config['model_selection'],
        '--threads', str(model_config['threads']),
        '--prefix', output_prefix,
        '--bs-trees', str(model_config['bootstrap_replicates'])
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running RAxML-NG: {e.stderr}")
        return False


def process_gene_tree(gene_name, config, input_dir, output_dir):
    """Process gene tree inference for a single gene"""
    gene_input_dir = input_dir / gene_name
    gene_output_dir = output_dir / gene_name
    gene_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Input file (use trimmed alignment if available, otherwise use aligned)
    input_file = gene_input_dir / 'aligned_trimmed.fasta'
    if not input_file.exists():
        input_file = gene_input_dir / 'aligned.fasta'
    
    if not input_file.exists():
        print(f"Warning: Alignment file not found for {gene_name}: {input_file}")
        return False
    
    # Choose tree inference tool
    tree_config = config['gene_tree']
    tool = tree_config.get('tool', 'iqtree')  # Default to IQ-TREE
    
    if tool == 'iqtree':
        success = infer_gene_tree_iqtree(input_file, gene_output_dir, config)
    elif tool == 'raxml-ng':
        success = infer_gene_tree_raxml(input_file, gene_output_dir, config)
    else:
        print(f"Warning: Unknown tree inference tool: {tool}, using IQ-TREE")
        success = infer_gene_tree_iqtree(input_file, gene_output_dir, config)
    
    if success:
        # Copy the resulting tree file to standard location
        tree_file = gene_output_dir / 'gene_tree.treefile'
        if tree_file.exists():
            final_tree_file = gene_output_dir / 'gene_tree.newick'
            with open(tree_file, 'r') as f:
                tree_content = f.read()
            with open(final_tree_file, 'w') as f:
                f.write(tree_content)
    
    return success


def main():
    parser = argparse.ArgumentParser(description='Gene tree inference for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--input-dir', default='results/alignments', help='Input directory')
    parser.add_argument('--output-dir', default='results/gene_trees', help='Output directory')
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
    
    for gene in tqdm(genes, desc='Inferring gene trees'):
        success = process_gene_tree(gene, config, input_dir, output_dir)
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\nGene tree inference complete!")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Results saved to: {output_dir}")


if __name__ == '__main__':
    main()
