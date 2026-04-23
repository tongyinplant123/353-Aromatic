# Stage 4: Species Tree Inference

## Overview

Infer species trees using both concatenation and coalescent methods.

## Command

```bash
hybsuite stage4 \
   -input_list input_list.txt \
   -aln_dir /path/to/STAGE3_output/06-Final_alignments \
   -output_dir /path/to/STAGE4_output \
   -sp_tree 146 \
   -nt 8 \
   -process 4 \
   -run_coalescent_step 12345
```

## Parameters Explained

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| `-sp_tree` | 146 | Support value for species tree (bootstrap/UFBoot) |
| `-run_coalescent_step` | 12345 | Enable coalescent analysis (any number enables) |

## Two Approaches

### 1. Concatenation Approach

**Method**: Combine all loci into one "supermatrix" and infer a single tree

**Process**:
1. Concatenate all locus alignments
2. Partition by locus (each locus has its own model)
3. Maximum likelihood inference
4. Bootstrap support assessment

**Advantages**:
- More site coverage
- Higher support values
- Well-established method

**Limitations**:
- May be affected by gene tree discordance (ILS)
- Assumes no conflicts between loci

### 2. Coalescent Approach

**Method**: Use gene tree distributions to infer species tree

**Process**:
1. Infer individual gene trees (353 trees)
2. Use ASTRAL to find species tree
3. Quartet-based support values

**Advantages**:
- Accounts for incomplete lineage sorting (ILS)
- More conservative
- Shows gene tree heterogeneity

**Limitations**:
- Requires many loci
- Lower support values (may be more accurate)

## Key Points ⚠️

### Understanding Support Values

1. **UFBoot (Ultrafast Bootstrap)**
   - Range: 0-100%
   - >95%: Strong support ✅
   - 80-95%: Moderate support ✅
   - <80%: Weak support ⚠️
   - <50%: No support ❌

2. **SH-aLRT**
   - Similar interpretation to UFBoot
   - Often used together with UFBoot
   - Both >95% = very strong support

3. **Local Posterior Probability (ASTRAL)**
   - Range: 0-1
   - >0.95: High support
   - 0.7-0.95: Moderate support
   - <0.7: Low support

### Interpreting Results

1. **High concordance**
   ```
   Concatenation: 92% of nodes with >95% support
   Coalescent: 87% of nodes with >0.95 PP
   
   Interpretation: Strong phylogenetic signal
   ```

2. **Some discordance**
   ```
   Topological differences: 5-10% of nodes
   Support differences: Moderate
   
   Interpretation: May indicate rapid radiation or ILS
   ```

3. **Major conflicts**
   ```
   Different topologies: >15% of nodes
   Low support in both: Many nodes <70%
   
   Interpretation: Investigate causes - biological or analytical?
   ```

### Critical Decisions

1. **Which tree to use?**
   - **Publication**: Usually concatenation for higher support
   - **Biological conclusions**: Coalescent may be more accurate
   - **Best practice**: Report both and compare

2. **Support threshold**
   - 95%: Standard for claims of strong support
   - 90%: Acceptable for moderate support
   - <80%: Should be interpreted cautiously

## Quality Checks

### Concatenation Results
```bash
# Check support values
cat STAGE4_output/*concatenation*.tre | grep -o "[0-9]*\.[0-9]*" | sort -n

# Look at tree file
cat STAGE4_output/supermatrix.treefile
```

### Coalescent Results
```bash
# Check quartet support
cat STAGE4_output/species_tree.newick

# Compare topologies
diff <(cat tree1.newick) <(cat tree2.newick)
```

### Support Value Distribution

**Good result**:
```
UFBoot distribution:
>99%: 45% of nodes
95-99%: 35% of nodes
80-95%: 12% of nodes
<80%: 8% of nodes

Interpretation: Strong overall support
```

**Problematic result**:
```
UFBoot distribution:
>99%: 15% of nodes
95-99%: 20% of nodes
80-95%: 25% of nodes
<80%: 40% of nodes  ⚠️ Too many unsupported nodes

Interpretation: Investigate data quality or model choice
```

## Common Issues

### Problem: "Very low support throughout tree"

**Causes**:
- Rapid radiation in your taxa
- High gene tree discordance (ILS)
- Insufficient data
- Model misspecification

**Solutions**:
1. Check data quality in Stages 1-3
2. Try different substitution models
3. Increase bootstrap replicates (if possible)
4. Consider that biological signal may be weak

### Problem: "Concatenation and coalescent trees very different"

**Causes**:
- Real biological conflict
- Incomplete lineage sorting
- Long-branch attraction
- Analytical issues

**Solutions**:
1. Check for contaminated sequences
2. Look for mislabeled samples
3. Investigate rogue taxa
4. Both trees may be valid - report both

### Problem: "Analysis taking too long"

**Causes**:
- Many loci (353 is standard for Angiosperms353)
- Complex models
- Limited compute resources

**Solutions**:
1. Subsample loci for testing
2. Use faster models (GTR+G vs GTR+I+G)
3. Reduce bootstrap replicates
4. Run on HPC

## Our Results

### Concatenation Tree
- **Method**: IQ-TREE with partition models
- **Support**: 89% of nodes >95% UFBoot
- **Tree file**: `supermatrix.treefile`

### Coalescent Tree  
- **Method**: ASTRAL
- **Support**: 82% of nodes >0.95 local PP
- **Tree file**: `species_tree.newick`

### Comparison
- **Topological differences**: ~7% of nodes
- **Major conflicts**: 2 nodes with different relationships
- **Interpretation**: Minor differences, overall congruent

## Output Files

```
STAGE4_output/
├── supermatrix.concatalist              # Loci included
├── supermatrix.phy                      # Concatenated alignment
├── supermatrix.model.txt                # Best models per partition
├── supermatrix.treefile                # Concatenation ML tree
├── supermatrix.iqtree                  # IQ-TREE output
├── quartet_support.txt                 # Quartet support values
├── species_tree.newick                  # Coalescent (ASTRAL) tree
├── gene_trees/                        # Individual gene trees
│   ├── gene_001.treefile
│   ├── gene_002.treefile
│   └── ...
└── stage4_log.txt
```

## Next Steps

With species trees complete, you can:

1. **Visualize trees** in FigTree, IQ-TREE viewer, or dendropy
2. **Compare topologies** between methods
3. **Proceed to molecular clock analysis** (Stage 5)
4. **Add fossil calibrations** for divergence times (Stage 6)

## Parameter Recommendations

### For High-Quality Data (Our Case)
```bash
-sp_tree 146         # Standard support
-nt 8                # Good parallelism
-process 4            # Balanced load
-run_coalescent_step 12345  # Enable both methods
```

### For Testing/Debugging
```bash
-sp_tree 100         # Fewer replicates for speed
-nt 4
-process 2
-run_coalescent_step 1      # Still runs coalescent
```

### For Very Large Datasets
```bash
-sp_tree 1000        # More support for difficult nodes
-nt 16              # More threads if available
-process 8
-run_coalescent_step 12345
```
