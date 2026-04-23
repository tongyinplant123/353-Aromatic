# HybSuite Stage-by-Stage Guide

This directory contains detailed guides for each stage of the HybSuite pipeline.

## Contents

1. [Stage 1: Data Acquisition](STAGE1_DATA_DOWNLOAD.md)
2. [Stage 2: Assembly & Paralog Detection](STAGE2_ASSEMBLY.md)
3. [Stage 3: Alignment & Filtering](STAGE3_ALIGNMENT.md)
4. [Stage 4: Species Tree Inference](STAGE4_TREE_INFERENCE.md)

## Quick Command Summary

```bash
# Stage 1
hybsuite stage1 -input_list input_list.txt -sra_maxsize 100GB -nt 4 -process 8 -output_dir STAGE1_output

# Stage 2
hybsuite stage2 -input_list input_list.txt -NGS_dir STAGE1_output/NGS_dataset -t Angiosperms353.fasta -output_dir STAGE2_output -seqs_min_length 100 -seqs_min_sample_coverage 0.1 -nt 6 -process 8

# Stage 3
hybsuite stage3 -input_list input_list.txt -eas_dir STAGE2_output/01-Assembled_data -paralogs_dir STAGE2_output/02-All_paralogs/03-Filtered_paralogs -t Angiosperms353.fasta -output_dir STAGE3_output -mafft_algorithm linsi -nt 8 -process 4 -aln_min_sample 0.5

# Stage 4
hybsuite stage4 -input_list input_list.txt -aln_dir STAGE3_output/06-Final_alignments -output_dir STAGE4_output -sp_tree 146 -nt 8 -process 4 -run_coalescent_step 12345
```

## Important Notes

- Replace `input_list.txt` with your actual input list
- Replace paths with your actual directory structure
- Adjust parameters based on your dataset size and research goals
