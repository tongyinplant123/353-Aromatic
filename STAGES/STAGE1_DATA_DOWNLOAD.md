# Stage 1: Data Acquisition

## Overview

Download NGS data (SRA/DRR) for each species in the study.

## Command

```bash
hybsuite stage1 \
   -input_list input_list.txt \
   -sra_maxsize 100GB \
   -nt 4 \
   -process 8 \
   -output_dir /path/to/STAGE1_output
```

## Parameters Explained

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| `-input_list` | input_list.txt | Tab-separated file with species and SRA IDs |
| `-sra_maxsize` | 100GB | Maximum file size per species to download |
| `-nt` | 4 | Number of threads for download |
| `-process` | 8 | Number of parallel download processes |
| `-output_dir` | /path/to/output | Where to save downloaded data |

## Input List Format

```
species_name    SRA_id    role
Cycas_revoluta    SRR23279596    Outgroup
Ginkgo_biloba    DRR838493    Outgroup
Amborella_trichopoda    SRR28891020
...
```

- Column 1: Species name (use underscores)
- Column 2: SRA or DRR accession number
- Column 3: "Outgroup" for outgroup species, empty for ingroup

## Key Points ⚠️

### Before Downloading

1. **Check available data**
   - Verify SRA/DRR accessions exist
   - Check estimated file sizes with `prefetch --max-size`
   - Some species may have multiple runs - choose wisely

2. **Storage planning**
   - Calculate total expected size: ~100GB × number of species
   - Ensure sufficient disk space
   - Use fast storage (SSD preferred) for better performance

3. **Network considerations**
   - Stable internet connection required
   - Large download may take hours/days
   - Consider running overnight

### During Download

1. **Monitor progress**
   - Check log files in output directory
   - Verify file sizes as they download
   - Look for any error messages

2. **Common issues**
   - Network timeout: Retry with fewer parallel processes
   - Insufficient space: Delete partial downloads and retry
   - Invalid accession: Verify SRA/DRR numbers

### After Download

1. **Verify completeness**
   - Check all expected files exist
   - Verify file sizes match expectations
   - Run FastQC if unsure about data quality

2. **Quality control**
   ```bash
   # Check downloaded files
   ls -lh STAGE1_output/NGS_dataset/
   
   # File structure should be:
   # STAGE1_output/NGS_dataset/
   # ├── SRR000001_1.fastq.gz
   # ├── SRR000001_2.fastq.gz
   # ├── SRR000002_1.fastq.gz
   # └── ...
   ```

## Quality Indicators

| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| File size per species | 1-10GB | <500MB or >50GB | <100MB or >100GB |
| Download success rate | >95% | 80-95% | <80% |
| FastQC scores | Q30 >85% | Q30 70-85% | Q30 <70% |

## Troubleshooting

### Problem: "Download failed" or "Connection timeout"

**Solutions**:
1. Reduce parallel processes: `-process 4` or `-process 2`
2. Check network stability
3. Try during off-peak hours
4. Use wget/curl to download manually if HybSuite fails

### Problem: "Insufficient disk space"

**Solutions**:
1. Free up space or use different output directory
2. Download species in batches
3. Delete intermediate files after Stage 2

### Problem: "Invalid SRA accession"

**Solutions**:
1. Verify accession number on NCBI SRA
2. Check if data is public
3. Some old accessions may have been retired

### Problem: Very large file size (>100GB)

**Solutions**:
1. Use `-sra_maxsize` to limit
2. Choose single-cell or smaller run if available
3. Contact data provider for alternatives

## Output Files

After Stage 1 completes, you should have:

```
STAGE1_output/
├── NGS_dataset/
│   ├── SRR23279596_1.fastq.gz
│   ├── SRR23279596_2.fastq.gz
│   ├── DRR838493_1.fastq.gz
│   └── ...
├── download_log.txt
└── species_list_with_size.txt
```

## Next Steps

Once Stage 1 is complete, proceed to [Stage 2: Assembly & Paralog Detection](STAGE2_ASSEMBLY.md)

## Common Parameters We Used

```bash
hybsuite stage1 \
   -input_list input_list_new7.0.txt \
   -sra_maxsize 100GB \
   -nt 4 \
   -process 8 \
   -output_dir /data/tongyin/.../HYB_output
```

**Our dataset**: 46 species (44 ingroup + 2 outgroup)
**Total download time**: ~12-24 hours depending on connection
