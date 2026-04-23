# Troubleshooting Guide

## Common Issues and Solutions

This guide covers problems you may encounter at each stage of the pipeline.

## Stage 1: Data Download

### Issue: "Connection timeout" or "Download failed"

**Symptoms**:
- Download stalls or fails
- Network errors in log

**Solutions**:
```bash
# 1. Reduce parallel processes
hybsuite stage1 -process 4 ...  # instead of 8

# 2. Try wget/curl directly
wget https://trace.ncbi.nlm.nih.gov/.../SRR000001.fastq.gz

# 3. Use fasterq-dump with retry
fastq-dump --split-files --retry 3 SRR000001
```

### Issue: "Insufficient disk space"

**Solutions**:
```bash
# 1. Free up space
rm -rf /tmp/*

# 2. Download in batches
hybsuite stage1 -input_list batch1.txt ...  # First 10 species
hybsuite stage1 -input_list batch2.txt ...  # Next 10 species
```

### Issue: "Invalid SRA accession"

**Solutions**:
1. Check accession on NCBI: https://www.ncbi.nlm.nih.gov/sra
2. Verify spelling (case-sensitive)
3. Check if data is public
4. Try alternative accession if available

## Stage 2: Assembly

### Issue: "Very low sequence count per species"

**Symptoms**:
- <50 sequences for some species
- Mean length <100bp

**Solutions**:
```bash
# 1. Check FastQC from Stage 1
fastqc STAGE1_output/NGS_dataset/SRR*.fastq.gz

# 2. Lower length threshold
-seqs_min_length 80

# 3. Lower coverage threshold
-seqs_min_sample_coverage 0.05

# 4. Check if it's a data quality issue
grep "SRR000001" STAGE2_output/*assemblies.txt
```

### Issue: "High paralog ratio (>40%)"

**Symptoms**:
- Many loci flagged as having paralogs
- Low single-copy gene count

**Solutions**:
1. This may be **biologically real** for your taxa
2. Check literature for known duplications
3. Use more stringent filtering in Stage 3
4. Accept lower locus count but higher quality

### Issue: "Assembly completely failed for a species"

**Solutions**:
1. Check if raw data exists from Stage 1
2. Verify file naming (should be SRR*_1.fastq.gz)
3. Try individual assembly:
   ```bash
   hybsuite stage2 -input_list single_species.txt ...
   ```
4. May need to exclude species if consistently failing

## Stage 3: Alignment

### Issue: "Very few loci after filtering"

**Symptoms**:
- <100 loci passing filter
- Many loci rejected

**Solutions**:
```bash
# 1. Lower sample threshold
-aln_min_sample 0.4   # or 0.3

# 2. Check problematic species
cat STAGE3_output/05-Filtered_locus_list/*rejected*

# 3. Re-run with less strict filtering
-aln_min_sample 0.5
```

### Issue: "Alignment algorithm too slow"

**Symptoms**:
- Stage 3 taking days
- Process stuck on same locus

**Solutions**:
```bash
# 1. Use faster algorithm
-mafft_algorithm auto   # instead of linsi

# 2. Reduce parallel processes
-process 2              # More memory per process

# 3. Subsample for testing
cp STAGE3_output/06-Final_alignments/gene_00*.fasta test_set/
```

### Issue: "Gappy alignments"

**Symptoms**:
- Some alignments >70% gaps
- Very short after trimming

**Solutions**:
1. TrimAl handles this, but check:
   ```bash
   cat STAGE3_output/04-Trimming_stats/*gap*
   ```
2. May indicate missing data
3. Consider excluding species with many gaps
4. Increase trimming stringency

## Stage 4: Tree Inference

### Issue: "Very low support values"

**Symptoms**:
- Most nodes <80% UFBoot
- Tree hard to interpret

**Causes**:
- Rapid radiation in your taxa
- High ILS (incomplete lineage sorting)
- Data quality issues

**Solutions**:
1. Check data quality in previous stages
2. Increase bootstrap:
   ```bash
   -sp_tree 1000
   ```
3. Try different substitution models
4. Accept biological uncertainty

### Issue: "Concatenation vs Coalescent conflict"

**Symptoms**:
- Different tree topologies
- Different support values

**Solutions**:
1. **Both may be correct** - they answer different questions
2. Report both in publication
3. Investigate specific conflicting nodes
4. Check for rogue taxa:
   ```bash
   # Use RogueNaRok or similar
   ```

### Issue: "Memory or time issues"

**Solutions**:
```bash
# 1. Reduce complexity
-sp_tree 100           # Fewer bootstrap

# 2. Use faster model
-m TEST                # Faster model selection

# 3. Subsample loci for testing
mkdir test_50
cp STAGE4_output/gene_trees/gene_00*.treefile test_50/
```

## General Issues

### Issue: "HybSuite command not found"

**Solutions**:
```bash
# 1. Check installation
conda activate hybsuite
which hybsuite

# 2. Reinstall if needed
conda install yuxuanliu::hybsuite

# 3. Use full path
/home/user/miniconda/envs/hybsuite/bin/hybsuite
```

### Issue: "Java error for ASTRAL"

**Solutions**:
```bash
# 1. Check Java installation
java -version

# 2. Install Java
conda install openjdk

# 3. Set JAVA_HOME
export JAVA_HOME=/path/to/java
```

### Issue: "File permission denied"

**Solutions**:
```bash
# 1. Check permissions
ls -la STAGE1_output/

# 2. Fix permissions
chmod -R 755 STAGE1_output/

# 3. Change ownership if needed
sudo chown -R user:user STAGE1_output/
```

## Getting Help

### Check Logs First

Every stage produces log files:
```bash
# Stage 1
cat STAGE1_output/download_log.txt

# Stage 2  
cat STAGE2_output/stage2_log.txt

# Stage 3
cat STAGE3_output/alignment_log.txt

# Stage 4
cat STAGE4_output/stage4_log.txt
```

### Verify File Structure
```bash
# Check expected files exist
ls -la STAGE1_output/NGS_dataset/
ls -la STAGE2_output/01-Assembled_data/
ls -la STAGE3_output/06-Final_alignments/
```

### Common Error Patterns

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| File not found | Wrong path | Verify with ls |
| Out of memory | Too many processes | Reduce -process |
| Segmentation fault | Memory issues | Reduce threads |
| Permission denied | File ownership | chmod or chown |
| Java error | Missing Java | Install openjdk |

## When to Start Over

Consider restarting a stage if:

1. **Output files corrupted or missing**
2. **Wrong parameters used**
3. **Data quality issues discovered late**
4. **Incomplete runs**

```bash
# Safe to delete and restart
rm -rf STAGE2_output
hybsuite stage2 ...
```

## Preventive Measures

1. **Always check logs after each stage**
2. **Verify output before proceeding**
3. **Keep notes of parameters used**
4. **Backup important results**
5. **Test on small subset first**
