# 353 Phylogenomics Pipeline - Data Management Guide

## Overview

This document explains what data should and should not be included in the GitHub repository.

## What to Include in GitHub ✅

### 1. Code and Scripts
- All Python scripts in `scripts/` directory
- Configuration templates in `config/`
- Pipeline orchestration scripts

### 2. Documentation
- README files
- User guides in `docs/`
- Example files in `examples/`

### 3. Configuration Files
- `environment.yml` - Conda environment
- `requirements.txt` - Python dependencies
- `config/parameters.yaml` - Default parameters
- `config/input_list.txt` - **Actual input list used**

### 4. Small Example Data (Optional)
- Small test datasets (<10MB)
- Example input files
- Sample sequence files for testing

## What NOT to Include in GitHub ❌

### 1. Large Data Files
- ❌ Raw sequence files (FASTQ/FASTA)
- ❌ Multiple sequence alignments
- ❌ Gene tree files
- ❌ Species tree files
- ❌ Any file >10MB

### 2. Intermediate Results
- ❌ `data/` directory contents
- ❌ `results/` directory contents
- ❌ Temporary files
- ❌ Log files

### 3. Old/Failed Runs
- ❌ Previous pipeline runs
- ❌ Failed analysis results
- ❌ Test data that's been superseded

## Your Actual Data Location

Your actual analysis data is located at:
```
/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/
```

This should remain on your local server/cluster and NOT be uploaded to GitHub.

## GitHub Repository Structure

```
353-aromatic/                    # GitHub repository
├── .gitignore                  # Ignore large files
├── README.md                   # Project overview
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment
├── config/
│   ├── parameters.yaml         # Default parameters
│   └── input_list.txt         # ✅ Actual input list (small)
├── examples/                   # Optional: small examples
│   └── input_list_example.txt
├── scripts/                    # All analysis scripts
│   ├── run_pipeline.py
│   ├── 01_data_preprocessing.py
│   ├── 02_alignment.py
│   ├── 03_gene_tree_inference.py
│   ├── 04_concatenation.py
│   ├── 05_coalescent.py
│   ├── 06_result_integration.py
│   └── README.md
└── docs/                       # Documentation
    ├── getting_started.md
    ├── parameter_guide.md
    ├── workflow_diagram.md
    └── github_setup.md
```

## Data Storage Strategy

### GitHub (Code Repository)
- ✅ Code
- ✅ Documentation
- ✅ Small configuration files
- ❌ Large data files

### Local Server/Cluster (Data Storage)
- ✅ Raw sequence data (FASTQ)
- ✅ Assembly results
- ✅ Alignment files
- ✅ Gene trees
- ✅ Species trees
- ✅ All analysis results

### Optional: Data Repositories (For Publication)
- **Zenodo**: For large datasets, get DOI
- **Figshare**: Alternative data repository
- **Dryad**: For ecological/evolutionary data

## Best Practices

### 1. Keep Repository Small
- Target: <100MB total size
- Maximum single file: <50MB
- Use `.gitignore` to exclude large files

### 2. Document Data Location
- In README, specify where actual data is stored
- Include instructions for data download
- Provide example data for testing

### 3. Version Control
- Use Git tags for different versions
- Document which version was used for publication
- Keep code and data versions synchronized

### 4. Backup Strategy
- Regular backups of local data
- Use version control for code
- Consider cloud storage for large datasets

## Example .gitignore

```gitignore
# Data files (large and sensitive)
data/
*.fasta
*.fa
*.fastq
*.bam
*.sam

# Results (can be regenerated)
results/
*.treefile
*.newick
*.pdf
*.png
*.svg

# Temporary files
*.tmp
*.log
*.bak

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
```

## Conclusion

**Rule of Thumb**: If it can be regenerated or downloaded, don't include it in GitHub. Only include code, documentation, and small configuration files.

Your actual data should remain on your local server at:
```
/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/
```

And only the **code and documentation** should go to GitHub.
