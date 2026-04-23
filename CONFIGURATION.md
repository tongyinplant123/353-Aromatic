# Configuration and Installation Guide

## Software Requirements

### Core Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| HybSuite | 1.1.6+ | Main pipeline | `conda install yuxuanliu::hybsuite` |
| IQ-TREE | 2.x | Tree inference | Included in HybSuite |
| ASTRAL | 5.x | Coalescent trees | Included in HybSuite |
| MAFFT | 7.x | Sequence alignment | Included in HybSuite |
| TrimAl | 1.x | Alignment trimming | Included in HybSuite |

### Optional but Recommended

| Software | Purpose | Installation |
|----------|---------|--------------|
| FastQC | Quality control | `conda install fastqc` |
| FigTree | Tree visualization | Download from website |
| Adobe Illustrator | Figure preparation | Commercial software |
| IQ-TREE Viewer | Interactive tree viewing | Download from website |

## HybSuite Installation

### Method 1: Conda (Recommended)

```bash
# Create new environment
conda create -n hybsuite python=3.9
conda activate hybsuite

# Install HybSuite
conda install yuxuanliu::hybsuite

# Verify installation
hybsuite -v
```

### Method 2: GitHub Source

```bash
# Clone repository
git clone https://github.com/Yuxuanliu-HZAU/HybSuite.git

# Add to PATH
export PATH=/path/to/HybSuite:$PATH

# Verify
hybsuite -v
```

## Environment Setup

### Our Working Environment

```bash
# Conda environment: hybsuite
# Python version: 3.9
# Platform: Linux HPC cluster
```

### Required Dependencies

When installing HybSuite via conda, these are automatically installed:

- Python 3.8+
- Biopython
- NumPy
- Pandas
- Java (for ASTRAL)
- Perl (for some scripts)

## Input Files

### 1. Angiosperms353 Bait File

**Description**: Target capture bait sequences for 353 nuclear genes

**Source**: Usually provided with HybSuite or downloaded separately

**File format**: FASTA
```
>gene_001
ATGCGATCGATCG...
>gene_002
GCTAGCTAGCTA...
```

**Location in our case**:
```
/data/tongyin/.../Angiosperms353.fasta
```

### 2. Input List File

**Description**: Tab-separated file mapping species to SRA accessions

**Format**:
```
species_name    SRA_id    role
```

**Example**:
```
Cycas_revoluta    SRR23279596    Outgroup
Ginkgo_biloba    DRR838493    Outgroup
Amborella_trichopoda    SRR28891020
```

**Important notes**:
- Use underscores instead of spaces in species names
- "Outgroup" indicates outgroup species
- Third column can be empty for ingroup

## Hardware Requirements

### Minimum

- **CPU**: 8 cores
- **RAM**: 32GB
- **Storage**: 500GB
- **Network**: Stable internet for SRA download

### Recommended

- **CPU**: 16+ cores
- **RAM**: 64GB+
- **Storage**: 2TB+ (for large projects)
- **Network**: High-speed connection

### Our Configuration

```bash
# HPC cluster settings used:
# - Nodes: 1
# - Cores per node: 8
# - RAM: 64GB
# - Storage: Shared filesystem
```

## Directory Structure

### Recommended Layout

```
project/
├── input/
│   ├── input_list.txt
│   ├── Angiosperms353.fasta
│   └── raw_data/           # Optional: pre-downloaded SRA
├── output/
│   ├── STAGE1_downloads/
│   ├── STAGE2_assembly/
│   ├── STAGE3_alignment/
│   └── STAGE4_trees/
├── scripts/               # Optional custom scripts
└── logs/                  # Keep logs for reproducibility
```

### Our Actual Structure

```
/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/
├── input_list_new7.0.txt
├── Angiosperms353.fasta
├── HYB_output/            # Stages 1-2
└── Output_185_2/         # Stages 3-4
```

## Parameter Selection Guide

### Stage 1: Data Download

| Parameter | When to Increase | When to Decrease |
|-----------|----------------|-----------------|
| `-process` | Fast network, large dataset | Slow network, limited resources |
| `-nt` | Many cores available | Memory limited |
| `-sra_maxsize` | Sufficient storage | Limited storage space |

### Stage 2: Assembly

| Parameter | When to Increase | When to Decrease |
|-----------|----------------|-----------------|
| `-seqs_min_length` | Want longer, more reliable sequences | Want more loci, accept shorter |
| `-seqs_min_sample_coverage` | Stringent locus selection | Want more loci |
| `-process` | Many cores, large dataset | Limited resources |

### Stage 3: Alignment

| Parameter | When to Increase | When to Decrease |
|-----------|----------------|-----------------|
| `-mafft_algorithm` | linsi for accuracy | auto for speed |
| `-aln_min_sample` | Want strict locus set | Want more loci |
| `-process` | Many cores available | Limited resources |

### Stage 4: Tree Inference

| Parameter | When to Increase | When to Decrease |
|-----------|----------------|-----------------|
| `-sp_tree` | Want more support replicates | Limited time/resources |
| `-nt` | Many cores available | Memory limited |
| `-process` | Parallel analysis | Sequential may be more stable |

## Environment Variables

Optional but sometimes useful:

```bash
# Java memory for ASTRAL
export JAVA_OPTS="-Xmx4g"

# MAFFT threads
export MAFFT_NUM_THREADS=8

# IQ-TREE memory
export IQTREE_MEM=8G
```

## Verification Commands

```bash
# Check HybSuite installation
hybsuite -v
hybsuite stage1 -h

# Check dependencies
which iqtree
which mafft
which trimal
java -version

# Verify input files
head -5 input_list.txt
head -5 Angiosperms353.fasta
```

## Common Setup Issues

### Issue: "hybsuite: command not found"

**Solution**:
```bash
# Check PATH
echo $PATH

# Add to PATH if needed
export PATH=/path/to/hybsuite/bin:$PATH

# Or reinstall
conda install yuxuanliu::hybsuite
```

### Issue: "Java not found" (for ASTRAL)

**Solution**:
```bash
# Install Java
conda install openjdk

# Verify
java -version
```

### Issue: "Permission denied" running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x /path/to/hybsuite/bin/*

# Or run with bash
bash /path/to/hybsuite/bin/hybsuite
```

## Next Steps

After setting up the environment:

1. [Stage 1: Data Download](STAGES/STAGE1_DATA_DOWNLOAD.md)
2. [Stage 2: Assembly](STAGES/STAGE2_ASSEMBLY.md)
3. [Stage 3: Alignment](STAGES/STAGE3_ALIGNMENT.md)
4. [Stage 4: Tree Inference](STAGES/STAGE4_TREE_INFERENCE.md)
