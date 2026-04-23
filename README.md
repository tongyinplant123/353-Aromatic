# Aromatic Plants Phylogenomics Project

## Project Overview

This repository contains the complete workflow and documentation for phylogenomic analysis of aromatic plants using the HybSuite pipeline. The project includes:

1. **HybSuite-based species tree inference** (353 nuclear genes)
2. **Molecular clock gene selection**
3. **Branch length estimation**
4. **Fossil calibration and divergence time estimation** (in progress)

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        353 Aromatic Plants Phylogenomics                     │
└─────────────────────────────────────────────────────────────────────────────┘

Stage 1: Data Acquisition
    ↓
Stage 2: Assembly & Paralog Detection
    ↓
Stage 3: Alignment & Filtering
    ↓
Stage 4: Species Tree Inference
    ↓
Stage 5: Molecular Clock Analysis ← (In Progress)
    ↓
Stage 6: Divergence Time Estimation ← (Planned)
```

## Quick Links

- **[Project Logic & Flow](LOGIC_FLOW.md)** - Detailed workflow explanation
- **[Stage-by-Stage Guide](STAGES/)** - Step-by-step instructions
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Commands Reference](COMMANDS.md)** - All commands used
- **[Configuration](CONFIGURATION.md)** - Software setup

## Key Features

### HybSuite Pipeline Stages

| Stage | Description | Key Points |
|-------|-------------|------------|
| Stage 1 | NGS Dataset Construction | SRA data download, size control |
| Stage 2 | Assembly & Paralog Detection | Assembly quality, paralog filtering |
| Stage 3 | Alignment Processing | MAFFT alignment, trimming |
| Stage 4 | Species Tree Inference | Concatenation + Coalescent methods |

### Molecular Clock Analysis

- Gene selection for clock-like behavior
- Branch length estimation
- Clock model testing

### Divergence Time Estimation

- Fossil calibration
- Time tree construction
- Results validation

## Project Status

- ✅ HybSuite stages 1-4 completed
- 🔄 Molecular clock analysis in progress
- ⏳ Divergence time estimation planned

## Data Location

**Actual data location** (not on GitHub):
```
/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/
├── HYB_output/                  # HybSuite results
└── Output_185_2/               # Final alignments and trees
```

## Citation

If you use this workflow, please cite:

1. **HybSuite**: Liu et al. (2025) Applications in Plant Sciences
2. **IQ-TREE**: Nguyen et al. (2015) Mol Biol Evol
3. **ASTRAL**: Zhang et al. (2018) Mol Phylogenet Evol

## Contact

For questions or issues, please open an issue on GitHub.

## Acknowledgments

This workflow is based on [HybSuite](https://github.com/Yuxuanliu-HZAU/HybSuite) by Yuxuan Liu et al.
