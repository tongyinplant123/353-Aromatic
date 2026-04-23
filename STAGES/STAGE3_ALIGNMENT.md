# Stage 3: Alignment & Filtering

## Overview

Perform multiple sequence alignment for each locus and apply quality filtering.

## Command

```bash
hybsuite stage3 \
   -input_list input_list.txt \
   -eas_dir /path/to/STAGE2_output/01-Assembled_data \
   -paralogs_dir /path/to/STAGE2_output/02-All_paralogs/03-Filtered_paralogs \
   -t /path/to/Angiosperms353.fasta \
   -output_dir /path/to/STAGE3_output \
   -mafft_algorithm linsi \
   -nt 8 \
   -process 4 \
   -aln_min_sample 0.5
```

## Parameters Explained

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| `-eas_dir` | STAGE2/01-Assembled_data | Cleaned assemblies from Stage 2 |
| `-paralogs_dir` | STAGE2/03-Filtered_paralogs | Paralog information |
| `-mafft_algorithm` | linsi | MAFFT alignment algorithm |
| `-aln_min_sample` | 0.5 | Minimum 50% species coverage per locus |

## MAFFT Algorithm Options

| Algorithm | Speed | Accuracy | Best For |
|-----------|-------|----------|----------|
| `linsi` | Slow | Highest | <200 sequences, high divergence |
| `einsi` | Medium | High | Medium-sized datasets, faster |
| `ginsi` | Medium | High | Global alignment needs |
| `auto` | Variable | Good | General use, automatic selection |

**Recommendation**: `linsi` for most phylogenomic datasets

## Key Points ⚠️

### Alignment Quality

1. **Why alignment matters**
   - Poor alignment = incorrect phylogeny
   - Gaps and missing data affect analysis
   - Trimming removes uncertain regions

2. **What to check**
   ```bash
   # Look at alignment statistics
   cat STAGE3_output/*_alignment_stats.txt
   
   # Check for weird alignments
   # - Very short final alignments
   # - Extremely gappy regions
   # - Inconsistent lengths
   ```

### Trimming Impact

1. **Before trimming**
   - Raw MAFFT alignment
   - May contain uncertain regions
   - Longer but potentially noisy

2. **After trimming**
   - TrimAl automated1 method
   - Removed gaps and poor regions
   - Shorter but more reliable

3. **Example**
   ```
   Locus gene_001:
   Before trim: 450bp
   After trim:  380bp (84% retained)
   
   ⚠️ If <60% retained, may indicate poor alignment
   ```

### Sample Coverage (Critical!)

1. **What is aln_min_sample?**
   - Minimum proportion of species that must have sequences
   - `0.5` = At least 50% of species must have data
   - Higher = stricter, fewer loci
   - Lower = more lenient, more loci

2. **Our setting: 0.5 (50%)**
   - Good balance for 46 species
   - Allows some missing data
   - Maintains phylogenetic signal

3. **How many loci will I get?**
   ```
   With aln_min_sample 0.5: ~180-200 loci (typical)
   With aln_min_sample 0.7: ~150-170 loci
   With aln_min_sample 0.8: ~120-150 loci
   ```

### Filtering Steps

1. **Paralog filtering** (from Stage 2)
   - Removed sequences identified as paralogs
   - Kept best single copy per species per locus

2. **Length filtering**
   - Removed sequences <100bp
   - Removed sequences below sample coverage threshold

3. **Alignment trimming**
   - TrimAl automated1
   - Removes poorly aligned positions
   - Removes terminal gaps

## Common Issues & Solutions

### Problem: "Very few loci after filtering (<100)"

**Causes**:
- Too strict sample coverage threshold
- Many species failing in Stage 2
- High paralog ratio reducing good loci

**Solutions**:
1. Lower `-aln_min_sample` to 0.4 or 0.3
2. Check which species are causing issues
3. Review Stage 2 assembly quality
4. May need to accept fewer loci

### Problem: "Alignments have very different lengths"

**Causes**:
- Some species may have incomplete data
- True sequence length variation
- Assembly issues

**Solutions**:
1. Check for frame shifts (indels)
2. Verify sequence directionality
3. Consider re-running with different algorithm
4. May need to exclude problematic loci

### Problem: "Gap-rich alignments"

**Causes**:
- Missing sequences in some species
- True biological absence
- Assembly failure

**Solutions**:
1. TrimAl handles this well
2. Check if specific species are problematic
3. Consider excluding species with many gaps
4. Gap proportion should be <50% for good loci

### Problem: "Alignment taking very long"

**Causes**:
- Large dataset (many species, many loci)
- Using slow algorithm (linsi)
- Limited compute resources

**Solutions**:
1. Switch to `einsi` or `auto` algorithm
2. Reduce `-process` to use less memory
3. Consider subsampling species
4. Run on HPC with more resources

## Quality Indicators

### Good Alignment
```
Locus: gene_142
Species: 42/46 (91%)
Length: 312bp (trimmed: 287bp)
Gaps: 12%
Status: ✅ PASS
```

### Problematic Alignment
```
Locus: gene_298
Species: 28/46 (61%)  ⚠️ Low coverage
Length: 890bp (trimmed: 180bp)  ⚠️ High gap content
Gaps: 67%  ⚠️ Too gappy
Status: ❌ FAIL
```

## Our Results

| Metric | Value |
|--------|-------|
| Input loci | 353 |
| After sample filter (0.5) | ~185 loci |
| Mean alignment length | ~280-320bp |
| Mean gap content | <15% |
| Final loci used | 185 |

## Output Files

```
STAGE3_output/
├── 01-Unfiltered_alignments/      # Raw MAFFT alignments
├── 02-Alignment_stats/           # Statistics before trimming
├── 03-Trimmed_alignments/        # TrimAl trimmed
├── 04-Trimming_stats/            # Statistics after trimming
├── 05-Filtered_locus_list/      # Loci passing filters
├── 06-Final_alignments/          # Ready for tree inference
│   ├── gene_001.fasta
│   ├── gene_002.fasta
│   └── ...
└── alignment_log.txt
```

## Next Steps

Proceed to [Stage 4: Species Tree Inference](STAGE4_TREE_INFERENCE.md)

## Parameter Tuning Guide

### More Stringent (Fewer, Higher Quality Loci)
```bash
-mafft_algorithm linsi     # Most accurate
-aln_min_sample 0.7       # 70% species required
```

### More Lenient (More, Lower Quality Loci)
```bash
-mafft_algorithm auto      # Faster
-aln_min_sample 0.4        # 40% species required
```

### Our Recommended Settings

For aromatic plants with 40-50 species:
```bash
-mafft_algorithm linsi
-aln_min_sample 0.5
-nt 8
-process 4
```
