#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Pipeline Script for 353 Phylogenomics
Orchestrates all pipeline stages
"""

import os
import sys
import argparse
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
import logging


def setup_logging(output_dir):
    """Setup logging configuration"""
    log_file = Path(output_dir) / 'pipeline.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def load_config(config_path):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def run_stage(stage_name, script_path, args, logger):
    """Run a pipeline stage"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Running Stage: {stage_name}")
    logger.info(f"{'='*60}\n")
    
    cmd = [sys.executable, str(script_path)] + args
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {stage_name}:")
        logger.error(e.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='353 Phylogenomics Pipeline')
    parser.add_argument('--config', required=True, help='Configuration file (YAML)')
    parser.add_argument('--stages', nargs='+', default=['all'],
                       choices=['all', '1', '2', '3', '4', '5', '6'],
                       help='Stages to run (1-6 or all)')
    parser.add_argument('--skip-stages', nargs='*', default=[],
                       choices=['1', '2', '3', '4', '5', '6'],
                       help='Stages to skip')
    parser.add_argument('--output-dir', default='results', help='Output directory')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    logger = setup_logging(output_dir)
    logger.info(f"353 Phylogenomics Pipeline")
    logger.info(f"Started at: {datetime.now()}")
    logger.info(f"Configuration: {args.config}")
    
    # Determine which stages to run
    if 'all' in args.stages:
        stages_to_run = ['1', '2', '3', '4', '5', '6']
    else:
        stages_to_run = args.stages
    
    stages_to_run = [s for s in stages_to_run if s not in args.skip_stages]
    
    logger.info(f"Stages to run: {', '.join(stages_to_run)}")
    
    # Define script paths
    script_dir = Path(__file__).parent
    scripts = {
        '1': script_dir / '01_data_preprocessing.py',
        '2': script_dir / '02_alignment.py',
        '3': script_dir / '03_gene_tree_inference.py',
        '4': script_dir / '04_concatenation.py',
        '5': script_dir / '05_coalescent.py',
        '6': script_dir / '06_result_integration.py'
    }
    
    # Define arguments for each stage
    stage_args = {
        '1': ['--config', args.config, '--output-dir', str(output_dir / 'preprocessing')],
        '2': ['--config', args.config, '--input-dir', str(output_dir / 'preprocessing' / 'sequences'),
              '--output-dir', str(output_dir / 'alignments')],
        '3': ['--config', args.config, '--input-dir', str(output_dir / 'alignments'),
              '--output-dir', str(output_dir / 'gene_trees')],
        '4': ['--config', args.config, '--input-dir', str(output_dir / 'alignments'),
              '--output-dir', str(output_dir / 'concatenation')],
        '5': ['--config', args.config, '--input-dir', str(output_dir / 'gene_trees'),
              '--output-dir', str(output_dir / 'coalescent')],
        '6': ['--config', args.config, '--output-dir', str(output_dir / 'figures')]
    }
    
    # Run stages
    success_count = 0
    fail_count = 0
    
    for stage in stages_to_run:
        script_path = scripts[stage]
        
        if not script_path.exists():
            logger.warning(f"Script not found for stage {stage}: {script_path}")
            fail_count += 1
            continue
        
        success = run_stage(
            f"Stage {stage}",
            script_path,
            stage_args[stage],
            logger
        )
        
        if success:
            success_count += 1
            logger.info(f"Stage {stage} completed successfully")
        else:
            fail_count += 1
            logger.error(f"Stage {stage} failed")
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("Pipeline Summary")
    logger.info(f"{'='*60}")
    logger.info(f"Successful stages: {success_count}")
    logger.info(f"Failed stages: {fail_count}")
    logger.info(f"Finished at: {datetime.now()}")
    logger.info(f"Log file: {output_dir / 'pipeline.log'}")
    
    if fail_count == 0:
        logger.info("\n🎉 Pipeline completed successfully!")
    else:
        logger.warning(f"\n⚠️ Pipeline completed with {fail_count} failed stage(s)")
        sys.exit(1)


if __name__ == '__main__':
    main()
