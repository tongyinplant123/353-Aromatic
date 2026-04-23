# 353 Pipeline - Scripts

This directory contains all analysis scripts for the phylogenomic pipeline.

## Scripts Overview

### 01_data_preprocessing.py
Data preprocessing and filtering:
- Sequence quality control
- Format conversion
- Gene-to-species mapping
- Paralog detection and filtering

### 02_alignment.py
Multiple sequence alignment:
- Automatic alignment with MAFFT/MUSCLE
- Alignment trimming with TrimAl
- Alignment filtering and quality control

### 03_gene_tree_inference.py
Gene tree inference for each locus:
- Model selection with ModelFinder
- Gene tree inference with IQ-TREE/RAxML-NG
- Branch support assessment (UFBoot, SH-aLRT)

### 04_concatenation.py
Concatenation analysis:
- Supermatrix construction
- Partition model selection
- ML analysis with branch support
- Result formatting

### 05_coalescent.py
Coalescent-based analysis:
- Gene tree collection and formatting
- Species tree inference with ASTRAL
- Support value calculation
- Gene tree heterogeneity assessment

### 06_result_integration.py
Result integration and visualization:
- Tree visualization with ete3
- Support value comparison
- Topology testing
- Figure generation

### run_pipeline.py
Main workflow script:
- Orchestrate all pipeline stages
- Handle dependencies between stages
- Parallel processing support
- Error handling and logging

## Usage

```bash
# Run full pipeline
python run_pipeline.py --config config/parameters.yaml

# Run individual script
python 01_data_preprocessing.py --config config/parameters.yaml

# Get help
python run_pipeline.py --help
```

## Dependencies

- Python 3.8+
- Biopython
- PyYAML
- tqdm
- ete3
- dendropy
- IQ-TREE or RAxML-NG
- MAFFT or MUSCLE
- ASTRAL
