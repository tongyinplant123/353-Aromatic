# 353 Phylogenomics Pipeline - Parameter Guide

## Configuration File: config/parameters.yaml

This document explains all configurable parameters in the pipeline.

## Data Paths

```yaml
data:
  input_dir: "data/sequences"        # Directory containing raw sequence files
  output_dir: "results"              # Main output directory
  alignments_dir: "data/alignments"  # Directory for alignments (intermediate)
  gene_trees_dir: "data/gene_trees"  # Directory for gene trees (intermediate)
```

## Input File

```yaml
input:
  list_file: "config/input_list.txt"  # Tab-separated file with species-gene mapping
  format: "tab"                        # Format: tab-separated
```

## Paralog Handling Strategy

```yaml
paralog_strategy: "single_copy"  # Options: "single_copy", "most_similar", "all", "orthology_inference"
```

**Options:**
- `single_copy`: Use only genes with exactly one sequence per species (recommended for most cases)
- `most_similar`: Select the most similar paralog for each species
- `all`: Include all paralogs (requires careful filtering)
- `orthology_inference`: Use orthology inference tools (e.g., OrthoFinder)

## Alignment Parameters

```yaml
alignment:
  tool: "mafft"              # Alignment tool: "mafft" or "muscle"
  algorithm: "auto"          # MAFFT algorithm: "auto", "linsi", "einsi", "ginsi"
  trim: true                 # Whether to trim alignments
  trim_tool: "trimal"        # Trimming tool: "trimal"
  trim_method: "automated1"  # Trimming method: "automated1", "gappyout", "strict"
```

**MAFFT Algorithms:**
- `auto`: Automatically selects the best algorithm
- `linsi`: Accurate for <200 sequences
- `einsi`: Uses consistency-based approach
- `ginsi`: Global alignment with iterative refinement

## Gene Tree Inference Parameters

```yaml
gene_tree:
  model_selection: "auto"              # Model selection: "auto" or specific model like "GTR+I+G"
  bootstrap_replicates: 1000           # Number of bootstrap replicates
  ufboot_replicates: 1000              # Number of UFBoot replicates
  sh_alrt: true                        # Perform SH-aLRT test
  threads: 8                           # Number of threads to use
```

## Concatenation Analysis Parameters

```yaml
concatenation:
  partition_file: "results/concatenation/partitions.nex"  # Partition file location
  partition_model: "UNLINKED"  # Partition model: "linked" or "unlinked"
  
  analysis:
    tool: "iqtree"             # Tree inference tool: "iqtree" or "raxml-ng"
    model: "MFP+MERGE"         # Model: "MFP+MERGE" (ModelFinder + merge)
    bootstrap: 1000            # Bootstrap replicates
    ufboot: 1000               # UFBoot replicates
    sh_alrt: true              # Perform SH-aLRT test
    threads: 16                # Number of threads
```

## Coalescent Analysis Parameters

```yaml
coalescent:
  tool: "astral"                    # Coalescent tool: "astral" or "mp_est"
  gene_tree_format: "newick"        # Gene tree format
  support_calculation: "local_posterior"  # Support: "quartet" or "local_posterior"
  threads: 8                        # Number of threads
```

## Result Visualization Parameters

```yaml
visualization:
  format: "pdf"              # Output format: "pdf", "png", "svg"
  dpi: 300                   # Resolution in DPI
  show_support: true         # Show branch support values
  support_threshold: 70      # Minimum support to display
  root_tree: true            # Root the tree
  outgroup: "Cycas_revoluta" # Outgroup species for rooting
```

## Quality Control Parameters

```yaml
quality_control:
  min_alignment_length: 100      # Minimum alignment length
  max_gap_threshold: 0.5         # Maximum gap proportion (0-1)
  min_species_per_gene: 0.8      # Minimum species coverage (0-1)
```

## Example Minimal Configuration

```yaml
data:
  input_dir: "data/sequences"
  output_dir: "results"

input:
  list_file: "config/input_list.txt"

paralog_strategy: "single_copy"

alignment:
  tool: "mafft"
  algorithm: "auto"
  trim: true

gene_tree:
  model_selection: "auto"
  bootstrap_replicates: 1000
  threads: 8

concatenation:
  analysis:
    tool: "iqtree"
    bootstrap: 1000
    threads: 16

coalescent:
  tool: "astral"
  threads: 8

visualization:
  format: "pdf"
  dpi: 300
  outgroup: "Cycas_revoluta"
```

## Running the Pipeline

After configuring parameters:

```bash
# Set up environment
conda env create -f environment.yml
conda activate phylo353

# Run pipeline
python scripts/run_pipeline.py --config config/parameters.yaml

# Or run individual stages
python scripts/01_data_preprocessing.py --config config/parameters.yaml
python scripts/04_concatenation.py --config config/parameters.yaml
python scripts/05_coalescent.py --config config/parameters.yaml
```

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all software is installed and in PATH
   ```bash
   conda activate phylo353
   which mafft iqtree2 trimal
   ```

2. **File format errors**: Check input file formats match specifications
   - Input list: tab-separated
   - Sequence files: proper FASTA format

3. **Memory issues**: Reduce thread counts or increase memory allocation

4. **Paralog filtering**: Adjust `min_species_per_gene` or use different paralog strategy
