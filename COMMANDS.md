# Commands Reference

This file contains all commands used in this project.

## Project Information

- **Species**: 44 aromatic plants + 2 outgroups
- **Genes**: Angiosperms353 (353 nuclear loci)
- **Data location**: `/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/`
- **Run date**: 2026-04-20

## HybSuite Commands

### Stage 1: Data Download

```bash
hybsuite stage1 \
   -input_list input_list_new7.0.txt \
   -sra_maxsize 100GB \
   -nt 4 \
   -process 8 \
   -output_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/HYB_output
```

**Notes**:
- Downloaded 46 species (44 ingroup + 2 outgroup)
- Total size: ~4.6TB before filtering
- Parallel download: 8 processes
- Threads per download: 4

### Stage 2: Assembly & Paralog Detection

```bash
hybsuite stage2 \
   -input_list /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/input_list_new7.0.txt \
   -NGS_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/HYB_output/NGS_dataset \
   -t /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/Angiosperms353.fasta \
   -output_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/HYB_output \
   -seqs_min_length 100 \
   -seqs_min_sample_coverage 0.1 \
   -nt 6 \
   -process 8
```

**Notes**:
- Bait file: Angiosperms353.fasta
- Min sequence length: 100bp
- Min sample coverage: 10%
- Parallel assembly: 8 processes
- Threads per assembly: 6

### Stage 3: Alignment & Filtering

```bash
hybsuite stage3 \
   -input_list /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/input_list_new7.0.txt \
   -eas_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/HYB_output/01-Assembled_data \
   -paralogs_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/HYB_output/02-All_paralogs/03-Filtered_paralogs \
   -t /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/Angiosperms353.fasta \
   -output_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/Output_185_2 \
   -PH 1234567b \
   -mafft_algorithm linsi \
   -nt 8 \
   -process 4 \
   -aln_min_sample 0.5
```

**Notes**:
- MAFFT algorithm: linsi (local pairwise, accurate)
- Min species coverage: 50%
- Final loci: 185 (after filtering)
- Parallel alignment: 4 processes
- Threads per alignment: 8

### Stage 4: Species Tree Inference

```bash
hybsuite stage4 \
   -input_list /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/input_list_new7.0.txt \
   -aln_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/Output_185_2/06-Final_alignments \
   -output_dir /data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/Output_185_2 \
   -PH 1234567b \
   -sp_tree 146 \
   -nt 8 \
   -process 4 \
   -run_coalescent_step 12345
```

**Notes**:
- Support replicates: 146
- Parallel tree inference: 4 processes
- Threads per tree: 8
- Coalescent analysis: enabled (12345)
- Output: Both concatenation and coalescent trees

## Input List Format

```
species_name    SRA_id    role
```

Example (`input_list_new7.0.txt`):
```
Cycas_revoluta    SRR23279596    Outgroup
Ginkgo_biloba    DRR838493    Outgroup
Amborella_trichopoda    SRR28891020
Nymphaea_colorata    SRR10198679
Piper_nigrum    SRR3404389
...
```

## Directory Structure

```
/data/tongyin/2.aromatic_plant_353/10_hybsuite_results_2_no_st_26.4.7/
├── input_list_new7.0.txt              # Input list
├── Angiosperms353.fasta                # Bait sequences
├── HYB_output/                        # HybSuite outputs
│   ├── NGS_dataset/                   # Downloaded SRA data
│   ├── 01-Assembled_data/            # Assembled sequences
│   ├── 02-All_paralogs/              # Paralog detection
│   │   ├── 01-Unfiltered_paralogs/
│   │   ├── 02-Paralog_clusters/
│   │   └── 03-Filtered_paralogs/
│   └── *_assemblies.txt              # Assembly statistics
└── Output_185_2/                     # Stage 3-4 outputs
    ├── 01-Unfiltered_alignments/
    ├── 02-Alignment_stats/
    ├── 03-Trimmed_alignments/
    ├── 04-Trimming_stats/
    ├── 05-Filtered_locus_list/
    ├── 06-Final_alignments/          # Ready for tree inference
    ├── supermatrix.*                 # Concatenation results
    ├── species_tree.newick           # Coalescent tree
    └── gene_trees/                   # Individual gene trees
```

## Quick Reference

| Stage | Command | Key Parameters |
|-------|---------|----------------|
| 1 | `hybsuite stage1` | `-sra_maxsize`, `-process` |
| 2 | `hybsuite stage2` | `-seqs_min_length`, `-seqs_min_sample_coverage` |
| 3 | `hybsuite stage3` | `-mafft_algorithm`, `-aln_min_sample` |
| 4 | `hybsuite stage4` | `-sp_tree`, `-run_coalescent_step` |

## Parameter Summary

| Parameter | Stage | Our Value | Default |
|-----------|-------|-----------|---------|
| sra_maxsize | 1 | 100GB | 100GB |
| seqs_min_length | 2 | 100 | 100 |
| seqs_min_sample_coverage | 2 | 0.1 | 0.1 |
| mafft_algorithm | 3 | linsi | auto |
| aln_min_sample | 3 | 0.5 | 0.5 |
| sp_tree | 4 | 146 | 100 |
