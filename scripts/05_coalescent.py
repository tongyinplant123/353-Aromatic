#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Coalescent-Based Analysis Script for 353 Phylogenomics Pipeline
Handles species tree inference with ASTRAL
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


def collect_gene_trees(gene_tree_dirs, config):
    """Collect gene trees from all genes"""
    gene_trees = []
    
    for gene_dir in tqdm(gene_tree_dirs, desc='Collecting gene trees'):
        gene_name = gene_dir.name
        
        # Look for gene tree file
        tree_file = gene_dir / 'gene_tree.newick'
        if not tree_file.exists():
            # Try alternative names
            tree_file = gene_dir / 'gene_tree.treefile'
        
        if tree_file.exists():
            gene_trees.append({
                'name': gene_name,
                'file': tree_file
            })
        else:
            print(f"Warning: Gene tree not found for {gene_name}")
    
    return gene_trees


def run_astral(gene_tree_files, output_dir, config):
    """Run ASTRAL for species tree inference"""
    output_dir = str(output_dir)
    
    # Create input file with all gene trees
    all_trees_file = Path(output_dir) / 'all_gene_trees.newick'
    
    with open(all_trees_file, 'w', encoding='utf-8') as f:
        for tree_file in gene_tree_files:
            with open(tree_file, 'r') as tf:
                f.write(tf.read().strip() + '\n')
    
    # Run ASTRAL
    cmd = [
        'java',  # ASTRAL requires Java
        '-jar', 'astral.jar',  # ASTRAL jar file
        '-i', str(all_trees_file),
        '-o', str(Path(output_dir) / 'species_tree.newick'),
        '-t', str(config['coalescent']['threads'])
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=output_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running ASTRAL: {e.stderr}")
        return False


def calculate_quartet_support(species_tree_file, gene_trees_file, output_dir):
    """Calculate quartet support using ASTRAL"""
    cmd = [
        'java',
        '-jar', 'astral.jar',
        '-q', str(Path(output_dir) / 'quartet_support.txt'),
        '-i', str(gene_trees_file),
        '-t', str(species_tree_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=output_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error calculating quartet support: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Coalescent-based analysis for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--input-dir', default='results/gene_trees', help='Input directory')
    parser.add_argument('--output-dir', default='results/coalescent', help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directories
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get list of gene tree directories
    gene_tree_dirs = [d for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(gene_tree_dirs)} gene tree directories")
    
    # Collect gene trees
    gene_trees = collect_gene_trees(gene_tree_dirs, config)
    print(f"Collected {len(gene_trees)} gene trees")
    
    if len(gene_trees) < 2:
        print("Error: Need at least 2 gene trees for coalescent analysis")
        sys.exit(1)
    
    # Run ASTRAL
    print("Running ASTRAL species tree inference...")
    success = run_astral(
        [gt['file'] for gt in gene_trees],
        output_dir,
        config
    )
    
    if success:
        print(f"\nCoalescent analysis complete!")
        print(f"Results saved to: {output_dir}")
        
        # Show tree file location
        tree_file = output_dir / 'species_tree.newick'
        if tree_file.exists():
            print(f"Species tree: {tree_file}")
            
            # Calculate quartet support if requested
            if config['coalescent'].get('quartet_support', False):
                print("Calculating quartet support...")
                gene_trees_file = output_dir / 'all_gene_trees.newick'
                calculate_quartet_support(tree_file, gene_trees_file, output_dir)
    else:
        print("Error: Coalescent analysis failed")


if __name__ == '__main__':
    main()
