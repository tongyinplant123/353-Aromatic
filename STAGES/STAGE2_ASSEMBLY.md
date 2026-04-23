# Stage 2: Assembly & Paralog Detection

## Overview

Assemble downloaded NGS reads against the Angiosperms353 bait sequences and detect potential paralogs.

## Command

```bash
hybsuite stage2 \
   -input_list input_list.txt \
   -NGS_dir /path/to/STAGE1_output/NGS_dataset \
   -t /path/to/Angiosperms353.fasta \
   -output_dir /path/to/STAGE2_output \
   -seqs_min_length 100 \
   -seqs_min_sample_coverage 0.1 \
   -nt 6 \
   -process 8
```

## Parameters Explained

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| `-input_list` | input_list.txt | Same as Stage 1 |
| `-NGS_dir` | STAGE1_output/NGS_dataset | Location of downloaded reads |
| `-t` | Angiosperms353.fasta | Bait sequences for assembly |
| `-seqs_min_length` | 100 | Minimum sequence length to keep |
| `-seqs_min_sample_coverage` | 0.1 | Minimum 10% sample coverage |
| `-nt` | 6 | Number of threads |
| `-process` | 8 | Number of parallel processes |

## Key Points ⚠️

### Assembly Quality

1. **What to check first**
   - Open `*_assemblies.txt` in output directory
   - Look for species with low sequence counts
   - Check mean sequence lengths

2. **Quality indicators per species**
   ```
   Species: Vanilla_planifolia
   Total sequences: 245
   Mean length: 287bp
   Coverage: 0.72
   Status: ✅ PASS
   ```

3. **Warning signs**
   - <50 sequences per species
   - Mean length <150bp
   - Coverage <0.3
   - Many "N" characters in sequences

### Paralog Detection

1. **Understanding paralogs**
   - Paralogous genes: Duplicated genes within a genome
   - In phylogenetics: Can cause incorrect tree topologies
   - Detection: Sequence similarity within species

2. **What HybSuite does**
   - Maps reads to bait sequences
   - Identifies multiple mappings (potential paralogs)
   - Filters based on similarity thresholds

3. **Interpreting results**
   ```
   Total loci: 353
   With paralogs: 89 (25%)
   Single-copy: 264 (75%)
   
   ⚠️ High paralog ratio may indicate:
   - True gene duplications in your taxa
   - Incomplete reference bait set
   - Assembly issues
   ```

### Critical Quality Checks

1. **Assembly statistics file**
   ```bash
   # Check key metrics
   cat STAGE2_output/0*-assemblies.txt | grep -E "Species|Total|Mean"
   
   # Look for failed assemblies
   grep -E "FAILED|ERROR|0 sequences" STAGE2_output/*-assemblies.txt
   ```

2. **Paralog summary**
   ```bash
   # View paralog statistics
   cat STAGE2_output/02-All_paralogs/paralog_summary.txt
   
   # Check filtered vs unfiltered
   ls -lh STAGE2_output/02-All_paralogs/03-Filtered_paralogs/
   ```

3. **Sample coverage**
   - Files in `01-Assembled_data/` should have most species
   - Low coverage species may need attention

## Common Issues & Solutions

### Problem: "Many species with <50 sequences"

**Causes**:
- Poor sequencing depth
- Low capture efficiency
- Assembly issues

**Solutions**:
1. Check original sequencing quality (FastQC)
2. Try lower `-seqs_min_length` (e.g., 80)
3. Consider excluding problematic species
4. Check if SRA data is actually target capture

### Problem: "Paralog ratio >40%"

**Causes**:
- True gene duplications in your taxa
- Bait sequences may be incomplete
- Overly sensitive detection

**Solutions**:
1. This may be biologically real for your taxa
2. Check literature for known duplications
3. Use more stringent filtering in Stage 3
4. Compare with other studies in your group

### Problem: "Some species completely missing"

**Causes**:
- Download failed (check Stage 1 logs)
- Assembly failed
- Species not in bait file

**Solutions**:
1. Verify files exist from Stage 1
2. Check log files for specific errors
3. Try individual species with different parameters
4. May need to exclude if consistently failing

### Problem: "Very short mean sequence length"

**Causes**:
- Degraded input DNA
- Wrong library type (SE vs PE)
- Assembly issues

**Solutions**:
1. Check FastQC for read quality
2. Verify correct library layout (paired-end)
3. Adjust min_length parameter if needed
4. May indicate poor sample quality

## Filtering Parameters

### Default vs Our Settings

| Parameter | Default | Our Value | Rationale |
|-----------|---------|-----------|-----------|
| seqs_min_length | 100 | 100 | Standard threshold |
| seqs_min_sample_coverage | 0.1 | 0.1 | Balance sensitivity |

### When to Adjust

**Increase stringency** (fewer but better loci):
```bash
-seqs_min_length 150    # Longer sequences only
-seqs_min_sample_coverage 0.2   # Higher coverage
```

**Decrease stringency** (more loci, lower quality):
```bash
-seqs_min_length 80     # Accept shorter sequences
-seqs_min_sample_coverage 0.05  # Lower coverage OK
```

## Output Files

```
STAGE2_output/
├── 01-Assembled_data/
│   ├── gene_001.fasta
│   ├── gene_002.fasta
│   └── ...
├── 02-All_paralogs/
│   ├── 01-Unfiltered_paralogs/
│   ├── 02-Paralog_clusters/
│   └── 03-Filtered_paralogs/
├── *_assemblies.txt         # Assembly statistics
├── *_paralog_summary.txt    # Paralog detection summary
└── download_log.txt
```

## Decision Points

### Should I exclude a species?

**Consider excluding if**:
- <20 sequences total
- Mean length <100bp
- Coverage <0.1
- Multiple failed QC checks

**Keep if**:
- >50 sequences
- Mean length >150bp
- Coverage >0.3
- Biologically important

## Next Steps

Proceed to [Stage 3: Alignment & Filtering](STAGE3_ALIGNMENT.md)

## Our Results

- **Species processed**: 46 (44 ingroup + 2 outgroup)
- **Total loci**: 353
- **Loci with paralogs**: ~25-30%
- **Final filtered loci**: Used in Stage 3
- **Problematic species**: None excluded (all passed QC)
