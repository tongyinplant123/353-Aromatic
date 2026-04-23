# 353-aromatic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository contains the reproducible pipeline for phylogenomic analysis of aromatic plants using 353 nuclear genes. The pipeline follows the workflow adapted from [HybSuite](https://github.com/Yuxuanliu-HZAU/HybSuite).

## Overview

This project implements a comprehensive phylogenomic analysis pipeline combining:
- **Concatenation approach**: Maximum likelihood analysis of concatenated supermatrix
- **Coalescent-based approach**: Species tree inference using gene tree distributions
- **Multiple paralog handling strategies**: Different methods to处理旁系同源基因

## Project Structure

```
353-aromatic/
├── README.md                    # This file
├── LICENSE                      # License information
├── requirements.txt             # Python dependencies
├── environment.yml              # Conda environment specification
├── .gitignore                   # Git ignore configuration
├── config/                      # Configuration files
│   ├── parameters.yaml          # Analysis parameters
│   └── input_list.txt         # Input data list
├── scripts/                     # Analysis scripts
│   ├── 01_data_preprocessing.py    # Data preprocessing and filtering
│   ├── 02_alignment.py             # Multiple sequence alignment
│   ├── 03_gene_tree_inference.py   # Gene tree inference for each locus
│   ├── 04_concatenation.py         # Concatenation analysis
│   ├── 05_coalescent.py            # Coalescent-based analysis
│   ├── 06_result_integration.py    # Result integration and visualization
│   └── run_pipeline.py             # Main workflow script
├── data/                        # Input data (not included in repo)
│   ├── sequences/               # Raw sequence data (FASTA)
│   ├── alignments/              # Multiple sequence alignments
│   └── gene_trees/              # Gene tree files
├── results/                     # Analysis results
│   ├── concatenation/           # Concatenation analysis results
│   ├── coalescent/              # Coalescent analysis results
│   └── figures/                 # Visualization outputs
└── docs/                        # Documentation
    ├── getting_started.md
    ├── parameter_guide.md
    ├── workflow_diagram.md
    └── github_setup.md
```

## Requirements

### Software Dependencies

- Python 3.8+
- IQ-TREE 2.x or RAxML-NG
- ASTRAL (or other coalescent software)
- MAFFT or MUSCLE for alignment
- Python packages: see `requirements.txt`

### Conda Environment

```bash
conda env create -f environment.yml
conda activate phylo353
```

## Input Data

### Required Input Files

1. **Sequence data**: FASTA files for each gene/locus
2. **Gene-to-species mapping**: Define which sequences belong to which species
3. **Outgroup specification**: Define outgroup species

### Input Format

The input list file (`config/input_list.txt`) should be formatted as:
```
species_name    gene_id    sequence_file    [paralog_id]
```

## Usage

### Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd 353-aromatic

# Set up conda environment
conda env create -f environment.yml
conda activate phylo353

# Run the complete pipeline
python scripts/run_pipeline.py --config config/parameters.yaml

# Or run individual steps
python scripts/01_data_preprocessing.py --config config/parameters.yaml
python scripts/04_concatenation.py --config config/parameters.yaml
python scripts/05_coalescent.py --config config/parameters.yaml
```

### Command Line Options

```bash
python scripts/run_pipeline.py --help
```

## Analysis Pipeline

### Step 1: Data Preprocessing
- Sequence quality control
- Format conversion
- Gene-to-species mapping
- Paralog detection and filtering

### Step 2: Multiple Sequence Alignment
- Automatic alignment with MAFFT/MUSCLE
- Alignment trimming with TrimAl

### Step 3: Gene Tree Inference
- Individual gene tree inference for each locus
- Model selection with ModelFinder (IQ-TREE)
- Branch support assessment

### Step 4: Concatenation Analysis
- Supermatrix construction
- ML analysis with IQ-TREE/RAxML-NG
- Partition model selection
- Branch support assessment (UFBoot, SH-aLRT)

### Step 5: Coalescent-Based Analysis
- Gene tree collection
- Species tree inference with ASTRAL
- Gene tree heterogeneity assessment

### Step 6: Result Integration
- Tree visualization with FigTree/IQ-TREE
- Support value comparison
- Topology testing

## Paralog Handling Strategies

This pipeline implements multiple strategies for handling paralogs:

1. **Single-copy orthologs only**: Use only genes with exactly one sequence per species
2. **Most similar paralog**: Select the most similar paralog for each species
3. **All paralogs included**: Include all paralogs with careful filtering
4. **Orthology inference**: Use orthology inference tools (e.g., OrthoFinder)

## Citation

If you use this pipeline in your research, please cite:

[To be added after publication]

### Key Software Citations

- IQ-TREE: Nguyen et al. (2015) Mol Biol Evol
- ASTRAL: Zhang et al. (2018) Mol Phylogenet Evol
- MAFFT: Katoh & Standley (2013) Mol Biol Evol
- HybSuite: Liu et al. (2025) Applications in Plant Sciences

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For questions or issues, please open an issue on GitHub.

## Acknowledgments

This work was supported by [Funding Agency].
