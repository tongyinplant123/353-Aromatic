# 353 Phylogenomics Pipeline - Getting Started Guide

## For New Users

This guide will help you get started with the 353 phylogenomics pipeline if you're new to this type of analysis.

## Prerequisites

Before you begin, ensure you have:

1. **Conda installed**: Download from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)

2. **Basic understanding of**:
   - Phylogenetics concepts
   - FASTA file format
   - Command line interface

## Step-by-Step Setup

### Step 1: Clone or Download the Repository

```bash
# If using git
git clone <your-repo-url>
cd 353-aromatic

# Or download and extract the zip file
```

### Step 2: Set Up the Conda Environment

```bash
# Create the conda environment
conda env create -f environment.yml

# Activate the environment
conda activate phylo353

# Verify installation
which mafft
which iqtree2
which trimal
```

### Step 3: Prepare Your Data

#### Organize Your Files

Create the following directory structure:

```
353-aromatic/
├── data/
│   └── sequences/
│       ├── gene_001.fasta
│       ├── gene_002.fasta
│       └── ...
└── config/
    └── input_list.txt
```

#### Create Input List

Edit `config/input_list.txt` with your data:

```
species_name    gene_id    sequence_file    [paralog_id]
Cycas_revoluta    gene_001    data/sequences/gene_001.fasta    1
Ginkgo_biloba    gene_001    data/sequences/gene_001.fasta    1
```

**Format explanation:**
- `species_name`: Species name (use underscores for spaces)
- `gene_id`: Gene/locus identifier (e.g., gene_001, gene_002)
- `sequence_file`: Path to FASTA file
- `paralog_id`: (Optional) Paralog identifier for genes with multiple copies

#### Prepare FASTA Files

Each gene should have its own FASTA file:

```fasta
>Cycas_revoluta_gene_001
ATGCGATCGATCGATCGATCG...

>Ginkgo_biloba_gene_001
ATGCGATCGATCGATCGATCG...

>Amborella_trichopoda_gene_001
ATGCGATCGATCGATCGATCG...
```

**Important:**
- Sequence IDs should include species name (first part before underscore)
- Use uppercase letters for sequences
- Ensure sequences are properly formatted

### Step 4: Configure Parameters (Optional)

Edit `config/parameters.yaml` to customize:

- **Paralog strategy**: Choose how to handle paralogs
- **Alignment parameters**: Select alignment tool and parameters
- **Tree inference**: Configure bootstrap replicates, threads, etc.
- **Visualization**: Set output format and outgroup

For most users, the default parameters work well.

### Step 5: Run the Pipeline

#### Option A: Run the Full Pipeline

```bash
python scripts/run_pipeline.py --config config/parameters.yaml
```

#### Option B: Run Stages Individually

```bash
# Stage 1: Data preprocessing
python scripts/01_data_preprocessing.py --config config/parameters.yaml

# Stage 2: Alignment
python scripts/02_alignment.py --config config/parameters.yaml

# Stage 3: Gene tree inference
python scripts/03_gene_tree_inference.py --config config/parameters.yaml

# Stage 4: Concatenation analysis
python scripts/04_concatenation.py --config config/parameters.yaml

# Stage 5: Coalescent analysis
python scripts/05_coalescent.py --config config/parameters.yaml

# Stage 6: Result integration
python scripts/06_result_integration.py --config config/parameters.yaml
```

### Step 6: Check Results

After completion, results will be in the `results/` directory:

```
results/
├── concatenation/
│   ├── supermatrix.phylip
│   ├── supermatrix.treefile
│   └── supermatrix.phylip.stats
├── coalescent/
│   └── species_tree.newick
└── figures/
    ├── concatenation_tree.pdf
    ├── coalescent_tree.pdf
    └── support_comparison.pdf
```

## Understanding the Output

### Concatenation Analysis

- **Method**: Combines all genes into a supermatrix
- **Model**: Maximum likelihood with partition models
- **Support**: UFBoot and SH-aLRT values
- **Output**: `supermatrix.treefile`

### Coalescent Analysis

- **Method**: Species tree from gene tree distributions
- **Tool**: ASTRAL
- **Support**: Local posterior probabilities
- **Output**: `species_tree.newick`

### Visualization

- **PDF files**: High-quality tree figures
- **Support values**: Branch support displayed on trees
- **Comparison**: Side-by-side comparison of methods

## Common Issues and Solutions

### Issue 1: "Command not found" for mafft/iqtree

**Solution**: Ensure conda environment is activated
```bash
conda activate phylo353
```

### Issue 2: Memory errors

**Solution**: Reduce thread count in `config/parameters.yaml`
```yaml
gene_tree:
  threads: 4  # Reduce from 8 to 4
```

### Issue 3: Missing sequences

**Solution**: Check your input list and sequence files
- Ensure file paths are correct
- Verify sequence IDs match species names

### Issue 4: Long runtime

**Solution**: 
- Reduce bootstrap replicates (e.g., from 1000 to 500)
- Use fewer genes for testing
- Increase thread count if memory allows

## Testing with Sample Data

If you don't have data yet, you can test the pipeline with dummy data:

1. Create a small subset of genes (2-3)
2. Use 5-10 species
3. Run the pipeline to verify everything works

## Next Steps

After getting the pipeline working:

1. **Add more genes**: Expand to your full dataset
2. **Optimize parameters**: Fine-tune based on your data
3. **Compare methods**: Analyze both concatenation and coalescent results
4. **Visualize**: Create publication-quality figures

## Getting Help

1. **Check documentation**: See `docs/` directory
2. **Review logs**: Check `results/pipeline.log`
3. **Issue tracking**: Open an issue on GitHub

## Citation

When using this pipeline, please cite:

[To be added after publication]

And the key software:
- IQ-TREE
- ASTRAL
- MAFFT

## Acknowledgments

This pipeline is adapted from [HybSuite](https://github.com/Yuxuanliu-HZAU/HybSuite).
