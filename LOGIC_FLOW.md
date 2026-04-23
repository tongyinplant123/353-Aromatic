# Project Logic and Workflow

## Overview

This document explains the complete logic and workflow of the 353 aromatic plants phylogenomics project.

## Research Objectives

1. **Species tree inference**: Reconstruct the phylogenetic relationships among 44 aromatic plant species using 353 nuclear genes
2. **Molecular clock analysis**: Identify clock-like genes for divergence time estimation
3. **Divergence time estimation**: Calibrate the tree with fossils to obtain temporal information

## Why HybSuite?

### Advantages

- **Specialized for target capture data**: Designed specifically for hybrid capture phylogenomics
- **Integrated paralog handling**: Built-in tools for detecting and filtering paralogs
- **Complete workflow**: From raw reads to species trees
- **Both methods**: Supports both concatenation and coalescent approaches

### Alternative Tools Considered

- **PHYLUCE**: Another popular pipeline for target capture data
- **ASTRAL/MP-EST**: Coalescent-only methods
- **RAxML/IQ-TREE**: Concatenation-only methods

HybSuite was chosen for its comprehensive and integrated approach.

## Workflow Logic

### Stage 1: Data Acquisition

**Objective**: Download NGS data from SRA/DRR databases

**Logic**:
1. Identify species of interest
2. Find available sequencing data (SRR/DRR accessions)
3. Download raw reads
4. Quality control

**Key Parameters**:
```bash
-sra_maxsize 100GB      # Maximum file size per species
-nt 4                   # Number of threads
-process 8             # Parallel processes
```

**⚠️ Important Points**:
- Check available data size before downloading
- Ensure sufficient storage space
- Verify data quality with FastQC
- Species with >100GB may need filtering

### Stage 2: Assembly & Paralog Detection

**Objective**: Assemble target sequences and detect paralogs

**Logic**:
1. Assemble reads against reference bait sequences (Angiosperms353)
2. Detect and filter potential paralogs
3. Quality control of assemblies

**Key Parameters**:
```bash
-seqs_min_length 100           # Minimum sequence length
-seqs_min_sample_coverage 0.1 # Minimum sample coverage
-nt 6                          # Threads
-process 8                     # Parallel processes
```

**⚠️ Important Points**:
- **Assembly quality varies by species**: Check `*_assemblies.txt` for statistics
- **Paralog quantity matters**: Too many paralogs may indicate issues
- **Sample coverage is critical**: Lower values may indicate failed assemblies
- **Review filtered results**: Check `03-Filtered_paralogs/` directory

**Quality Indicators**:
- ✅ >80% species with >100 sequences
- ✅ Mean sequence length >200bp
- ✅ Paralog ratio <30%

### Stage 3: Alignment & Filtering

**Objective**: Multiple sequence alignment and quality control

**Logic**:
1. Align sequences for each locus
2. Trim poorly aligned regions
3. Filter low-quality alignments
4. Select final set of loci

**Key Parameters**:
```bash
-mafft_algorithm linsi       # Local alignment for accuracy
-aln_min_sample 0.5          # Minimum 50% species coverage
-nt 8                         # Threads
-process 4                    # Parallel processes
```

**⚠️ Important Points**:
- **linsi vs einsi**: linsi more accurate but slower
- **Sample coverage threshold**: Lower = more loci, higher = more reliable
- **Alignment trimming**: Essential for removing uncertain regions
- **Final locus count**: Our run produced 185 loci after filtering

**Quality Indicators**:
- ✅ Consistent alignment lengths
- ✅ Minimal missing data
- ✅ Proper gap distribution

### Stage 4: Species Tree Inference

**Objective**: Reconstruct species trees using multiple methods

**Logic**:
1. **Concatenation approach**: Combine all loci into supermatrix
   - Partition model analysis
   - Maximum likelihood inference
   - Bootstrap support assessment

2. **Coalescent approach**: Gene tree distributions
   - Individual gene trees
   - ASTRAL species tree
   - Quartet support

**Key Parameters**:
```bash
-sp_tree 146              # Species tree topology support
-run_coalescent_step 12345  # Enable coalescent analysis
-nt 8                     # Threads
-process 4                # Parallel processes
```

**⚠️ Important Points**:
- **Concatenation vs Coalescent**: Both provide complementary insights
- **Support values**: UFBoot >95% generally considered strong
- **Tree topology**: Compare results from both methods
- **Incongruence**: May indicate biological signal or analytical issues

**Output Files**:
- `supermatrix.treefile`: Concatenation tree
- `species_tree.newick`: Coalescent tree
- Various statistics files

### Stage 5: Molecular Clock Analysis (In Progress)

**Objective**: Identify clock-like genes for divergence time estimation

**Logic**:
1. Test clock-like behavior of each gene
2. Select genes with clock-like evolution
3. Estimate branch lengths
4. Combine with species tree

**Methods**:
- **Reltime**: Fast molecular clock
- **MCMCTree**: Bayesian divergence time
- **PASTA**: Protein clock genes

**⚠️ Important Points**:
- Not all genes are clock-like
- Selection criteria based on AIC/BIC
- Requires fossil calibration points

### Stage 6: Divergence Time Estimation (Planned)

**Objective**: Obtain temporal phylogenetic tree

**Logic**:
1. Identify fossil calibration points
2. Set up dating analysis
3. Run MCMC sampling
4. Validate results

**⚠️ Important Points**:
- **Fossil selection**: Needs paleontological expertise
- **Prior distribution**: Based on fossil age ranges
- **MCMC convergence**: Requires testing
- **Validation**: Cross-check with published dates

## Decision Points

### Data Quality Issues

| Problem | Indicator | Action |
|---------|-----------|--------|
| Low assembly success | <80% species with sequences | Check SRA data quality |
| High paralog ratio | >40% loci with paralogs | Increase filtering stringency |
| Poor alignment | Many gaps/missing | Adjust MAFFT parameters |
| Long branch attraction | Unusual tree topology | Increase support values |

### Parameter Tuning

| Stage | Parameter | Default | Our Value | Reason |
|-------|-----------|---------|-----------|--------|
| Stage 2 | seqs_min_length | 100 | 100 | Standard threshold |
| Stage 2 | seqs_min_sample_coverage | 0.1 | 0.1 | Balance sensitivity |
| Stage 3 | aln_min_sample | 0.5 | 0.5 | Our dataset size |
| Stage 4 | sp_tree support | 146 | 146 | Standard |

## Comparison of Methods

### Concatenation vs Coalescent

| Aspect | Concatenation | Coalescent |
|--------|---------------|------------|
| **Assumes** | No gene tree discordance | Gene tree discordance exists |
| **Strengths** | More site coverage | Accounts for ILS |
| **Weaknesses** | May be misled by ILS | Requires many loci |
| **Best for** | Dense sampling | Resolving rapid radiations |

### Our Results

- **Concatenation tree**: Higher support values overall
- **Coalescent tree**: More conservative, may reveal hidden conflicts
- **Agreement**: Most nodes concordant between methods

## Key Lessons Learned

1. **Data quality is paramount**: Invest time in QC
2. **Paralog filtering is critical**: Conservative approach recommended
3. **Multiple methods**: Use both concatenation and coalescent
4. **Documentation**: Record all parameter changes
5. **Iteration**: First run rarely optimal

## References

- HybSuite: Liu et al. (2025) Applications in Plant Sciences
- IQ-TREE: Nguyen et al. (2015) Mol Biol Evol
- ASTRAL: Zhang et al. (2018) Mol Phylogenet Evol
