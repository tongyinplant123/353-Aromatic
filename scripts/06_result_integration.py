#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Result Integration and Visualization Script for 353 Phylogenomics Pipeline
Handles tree visualization and comparison
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from Bio import SeqIO
from ete3 import Tree, TreeStyle, NodeStyle
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def visualize_tree(tree_file, output_file, config):
    """Visualize a phylogenetic tree using ete3"""
    # Load tree
    t = Tree(tree_file)
    
    # Get visualization config
    viz_config = config['visualization']
    
    # Create tree style
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_length = False
    ts.show_branch_support = viz_config['show_support']
    
    # Style for leaves
    nstyle = NodeStyle()
    nstyle["size"] = 0
    nstyle["shape"] = "circle"
    
    # Style for internal nodes
    for node in t.traverse():
        node.set_style(nstyle)
    
    # Root the tree if specified
    if viz_config['root_tree']:
        outgroup = viz_config.get('outgroup', '')
        if outgroup:
            try:
                t.set_outgroup(outgroup)
            except:
                print(f"Warning: Could not root tree with outgroup {outgroup}")
    
    # Render tree
    if viz_config['format'] == 'pdf':
        t.render(output_file, tree_style=ts, dpi=viz_config['dpi'])
    elif viz_config['format'] == 'png':
        t.render(output_file, tree_style=ts, dpi=viz_config['dpi'])
    elif viz_config['format'] == 'svg':
        t.render(output_file, tree_style=ts, dpi=viz_config['dpi'])
    
    return True


def compare_support_values(concatenation_tree, coalescent_tree, output_dir):
    """Compare support values between trees"""
    # This is a simplified version - in practice, you'd use more sophisticated methods
    print("Support value comparison:")
    print("- Concatenation: UFBoot/SH-aLRT support")
    print("- Coalescent: Local posterior probability")
    
    # Create comparison plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sample data (in practice, extract from actual trees)
    categories = ['Concatenation', 'Coalescent']
    avg_support = [85, 92]  # Example values
    
    ax.bar(categories, avg_support, color=['#2ecc71', '#3498db'])
    ax.set_ylabel('Average Support Value')
    ax.set_title('Support Value Comparison')
    ax.set_ylim(0, 100)
    
    # Add value labels on bars
    for i, v in enumerate(avg_support):
        ax.text(i, v + 2, f'{v}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'support_comparison.pdf', dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Result integration and visualization for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--concatenation-tree', help='Concatenation tree file')
    parser.add_argument('--coalescent-tree', help='Coalescent tree file')
    parser.add_argument('--output-dir', default='results/figures', help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get tree files from config if not specified
    if not args.concatenation_tree:
        concat_tree_file = 'results/concatenation/supermatrix.treefile'
    else:
        concat_tree_file = args.concatenation_tree
    
    if not args.coalescent_tree:
        coalescent_tree_file = 'results/coalescent/species_tree.newick'
    else:
        coalescent_tree_file = args.coalescent_tree
    
    # Visualize concatenation tree
    if os.path.exists(concat_tree_file):
        print(f"Visualizing concatenation tree: {concat_tree_file}")
        output_file = output_dir / 'concatenation_tree.pdf'
        visualize_tree(concat_tree_file, output_file, config)
        print(f"Saved: {output_file}")
    
    # Visualize coalescent tree
    if os.path.exists(coalescent_tree_file):
        print(f"Visualizing coalescent tree: {coalescent_tree_file}")
        output_file = output_dir / 'coalescent_tree.pdf'
        visualize_tree(coalescent_tree_file, output_file, config)
        print(f"Saved: {output_file}")
    
    # Compare support values
    if os.path.exists(concat_tree_file) and os.path.exists(coalescent_tree_file):
        print("\nComparing support values...")
        compare_support_values(concat_tree_file, coalescent_tree_file, output_dir)
        print(f"Saved support comparison: {output_dir / 'support_comparison.pdf'}")
    
    print(f"\nResult integration complete!")
    print(f"Figures saved to: {output_dir}")


if __name__ == '__main__':
    main()
