# 353 Phylogenomics Pipeline - Workflow Diagram

## Overview

This document describes the complete analysis workflow for the 353 phylogenomic pipeline.

## Pipeline Stages

```
Stage 1: Data Preprocessing
    ↓
Stage 2: Multiple Sequence Alignment
    ↓
Stage 3: Gene Tree Inference
    ↓
Stage 4: Species Tree Inference
    ├─ Concatenation Approach
    └─ Coalescent-Based Approach
    ↓
Stage 5: Result Integration and Visualization
```

## Detailed Workflow

### Stage 1: Data Preprocessing

```
Input: Raw sequence files (FASTA)
    ↓
- Quality control
- Format conversion
- Gene-to-species mapping
- Paralog detection
    ↓
Output: Processed sequence files
```

### Stage 2: Multiple Sequence Alignment

```
Input: Processed sequences
    ↓
- Multiple sequence alignment (MAFFT/MUSCLE)
- Alignment trimming (TrimAl)
- Alignment filtering
    ↓
Output: Aligned sequences (FASTA/PHYLIP)
```

### Stage 3: Gene Tree Inference

```
Input: Multiple sequence alignments
    ↓
- Model selection (ModelFinder)
- Gene tree inference (IQ-TREE/RAxML)
- Branch support assessment
    ↓
Output: Gene tree files (NEWICK)
```

### Stage 4: Species Tree Inference

#### Concatenation Approach

```
Input: Multiple sequence alignments
    ↓
- Supermatrix construction
- Partition model selection
- ML analysis with branch support
    ↓
Output: Concatenation species tree
```

#### Coalescent-Based Approach

```
Input: Gene trees
    ↓
- Gene tree collection
- Quartet-based species tree inference (ASTRAL)
- Local posterior support
    ↓
Output: Coalescent species tree
```

### Stage 5: Result Integration

```
Input: Both species trees
    ↓
- Tree visualization
- Support value comparison
- Topology testing
    ↓
Output: Final figures and statistics
```

## Input Data Requirements

### Required Files

1. **Sequence data**: FASTA files for each gene/locus
2. **Input list**: Tab-separated file with species-gene mapping
3. **Configuration file**: YAML file with analysis parameters

### Input List Format

```
species_name    gene_id    sequence_file    [paralog_id]
```

Example:
```
Cycas_revoluta    gene_001    sequences/gene_001.fasta    1
Ginkgo_biloba    gene_001    sequences/gene_001.fasta    1
```

## Output Structure

```
results/
├── concatenation/
│   ├── supermatrix.phylip
│   ├── supermatrix.phylip.treefile
│   └── supermatrix.phylip.stats
├── coalescent/
│   ├── gene_trees/
│   └── species_tree.newick
└── figures/
    ├── concatenation_tree.pdf
    ├── coalescent_tree.pdf
    └── support_comparison.pdf
```

## Key Parameters

### Paralog Handling

- **single_copy**: Use only single-copy orthologs
- **most_similar**: Select most similar paralog
- **all**: Include all paralogs
- **orthology_inference**: Use orthology inference tools

### Alignment Parameters

- **Tool**: MAFFT or MUSCLE
- **Algorithm**: auto, linsi, einsi, ginsi (MAFFT)
- **Trimming**: trimal with automated1 method

### Tree Inference

- **Model selection**: ModelFinder (auto)
- **Bootstrap**: 1000 replicates
- **UFBoot**: 1000 replicates
- **SH-aLRT**: true

## Command Line Interface

### Full Pipeline

```bash
python scripts/run_pipeline.py --config config/parameters.yaml
```

### Individual Stages

```bash
python scripts/01_data_preprocessing.py --config config/parameters.yaml
python scripts/02_alignment.py --config config/parameters.yaml
python scripts/03_gene_tree_inference.py --config config/parameters.yaml
python scripts/04_concatenation.py --config config/parameters.yaml
python scripts/05_coalescent.py --config config/parameters.yaml
python scripts/06_result_integration.py --config config/parameters.yaml
```

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all software is installed and in PATH
2. **File format errors**: Check input file formats match specifications
3. **Memory issues**: Adjust thread counts and memory allocation
4. **Paralog filtering**: Adjust filtering thresholds in parameters.yaml

## References

- HybSuite: Liu et al. (2025) Applications in Plant Sciences
- IQ-TREE: Nguyen et al. (2015) Mol Biol Evol
- ASTRAL: Zhang et al. (2018) Mol Phylogenet Evol
- MAFFT: Katoh & Standley (2013) Mol Biol Evol
