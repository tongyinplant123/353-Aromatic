#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Preprocessing Script for 353 Phylogenomics Pipeline
Handles sequence quality control, format conversion, and paralog detection
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from Bio import SeqIO
import pandas as pd
from tqdm import tqdm


def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def read_input_list(input_list_path):
    """Read the input list file and return as DataFrame"""
    df = pd.read_csv(input_list_path, sep='\t', header=None, 
                     names=['species', 'gene', 'sequence_file', 'paralog'])
    return df


def check_sequence_quality(seq_file):
    """Check sequence quality and return statistics"""
    records = list(SeqIO.parse(seq_file, 'fasta'))
    
    stats = {
        'total_sequences': len(records),
        'avg_length': sum(len(rec) for rec in records) / len(records) if records else 0,
        'min_length': min(len(rec) for rec in records) if records else 0,
        'max_length': max(len(rec) for rec in records) if records else 0
    }
    
    return stats


def filter_sequences_by_length(records, min_length):
    """Filter sequences by minimum length"""
    return [rec for rec in records if len(rec) >= min_length]


def detect_paralogs(records):
    """Detect paralogs based on sequence similarity"""
    # Simple paralog detection: if multiple sequences from same species
    species_counts = {}
    for rec in records:
        species = rec.id.split('_')[0] if '_' in rec.id else rec.id
        species_counts[species] = species_counts.get(species, 0) + 1
    
    paralogs = {species: count for species, count in species_counts.items() if count > 1}
    return paralogs, species_counts


def process_single_gene(gene_df, config, output_dir):
    """Process sequences for a single gene locus"""
    gene_name = gene_df['gene'].iloc[0]
    
    # Create output directory for this gene
    gene_output_dir = output_dir / 'sequences' / gene_name
    gene_output_dir.mkdir(parents=True, exist_ok=True)
    
    all_records = []
    
    # Read and process each sequence file
    for _, row in gene_df.iterrows():
        seq_file = row['sequence_file']
        
        if not os.path.exists(seq_file):
            print(f"Warning: Sequence file not found: {seq_file}")
            continue
        
        records = list(SeqIO.parse(seq_file, 'fasta'))
        all_records.extend(records)
    
    # Check sequence quality
    quality_stats = check_sequence_quality(str(gene_output_dir / 'all.fasta'))
    
    # Filter by length
    min_length = config['quality_control']['min_alignment_length']
    filtered_records = filter_sequences_by_length(all_records, min_length)
    
    # Detect paralogs
    paralogs, species_counts = detect_paralogs(filtered_records)
    
    # Apply paralog strategy
    paralog_strategy = config['paralog_strategy']
    final_records = apply_paralog_strategy(filtered_records, paralog_strategy, species_counts)
    
    # Write processed sequences
    output_file = gene_output_dir / 'processed.fasta'
    SeqIO.write(final_records, output_file, 'fasta')
    
    # Write statistics
    stats_file = gene_output_dir / 'statistics.txt'
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(f"Gene: {gene_name}\n")
        f.write(f"Original sequences: {len(all_records)}\n")
        f.write(f"After length filtering: {len(filtered_records)}\n")
        f.write(f"Final sequences: {len(final_records)}\n")
        f.write(f"Paralogs detected: {len(paralogs)}\n")
    
    return {
        'gene': gene_name,
        'original': len(all_records),
        'filtered': len(filtered_records),
        'final': len(final_records),
        'paralogs': len(paralogs)
    }


def apply_paralog_strategy(records, strategy, species_counts):
    """Apply the specified paralog handling strategy"""
    if strategy == 'single_copy':
        # Keep only species with exactly one sequence
        single_copy_species = [species for species, count in species_counts.items() if count == 1]
        return [rec for rec in records if rec.id.split('_')[0] in single_copy_species]
    
    elif strategy == 'most_similar':
        # For each species, keep the most similar paralog (simplified: keep first)
        species_records = {}
        for rec in records:
            species = rec.id.split('_')[0] if '_' in rec.id else rec.id
            if species not in species_records:
                species_records[species] = []
            species_records[species].append(rec)
        
        final_records = []
        for species, recs in species_records.items():
            # Keep the first sequence (simplified)
            final_records.append(recs[0])
        
        return final_records
    
    elif strategy == 'all':
        # Keep all sequences
        return records
    
    else:
        print(f"Warning: Unknown paralog strategy '{strategy}', using 'single_copy'")
        return apply_paralog_strategy(records, 'single_copy', species_counts)


def main():
    parser = argparse.ArgumentParser(description='Data preprocessing for 353 phylogenomics')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--output-dir', default='results/preprocessing', help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directories
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read input list
    input_list_path = config['input']['list_file']
    input_df = read_input_list(input_list_path)
    
    print(f"Loaded {len(input_df)} entries from input list")
    
    # Get unique genes
    genes = input_df['gene'].unique()
    print(f"Found {len(genes)} unique genes")
    
    # Process each gene
    results = []
    for gene in tqdm(genes, desc='Processing genes'):
        gene_df = input_df[input_df['gene'] == gene]
        result = process_single_gene(gene_df, config, output_dir)
        results.append(result)
    
    # Write summary
    summary_df = pd.DataFrame(results)
    summary_file = output_dir / 'summary.tsv'
    summary_df.to_csv(summary_file, sep='\t', index=False)
    
    print(f"\nPreprocessing complete!")
    print(f"Results saved to: {output_dir}")
    print(f"Summary saved to: {summary_file}")
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Total genes processed: {len(genes)}")
    print(f"Total sequences (original): {summary_df['original'].sum()}")
    print(f"Total sequences (final): {summary_df['final'].sum()}")
    print(f"Genes with paralogs: {summary_df['paralogs'].sum()}")


if __name__ == '__main__':
    main()
