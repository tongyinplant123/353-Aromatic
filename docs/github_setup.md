# 353 Phylogenomics Pipeline - GitHub Setup Guide

## Quick Start for GitHub

This guide will help you set up your GitHub repository for the 353 phylogenomics pipeline.

## Step 1: Initialize Git Repository

```bash
# Navigate to your project directory
cd 353-aromatic

# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/tongyinplant123/353-aromatic.git

# Create .gitignore (already included)
# Make sure .gitignore includes data/ and results/ directories
```

## Step 2: Add Files to Repository

```bash
# Add all files
git add .

# Or add specific files
git add README.md
git add LICENSE
git add requirements.txt
git add environment.yml
git add config/
git add scripts/
git add docs/

# Check status
git status
```

## Step 3: Commit Changes

```bash
# Commit with descriptive message
git commit -m "Initial commit: 353 phylogenomics pipeline with HybSuite workflow"

# Add more commits as you develop
git add new_script.py
git commit -m "Add new feature: support for additional paralog handling"
```

## Step 4: Push to GitHub

```bash
# Push to GitHub
git push -u origin main

# Or if using master branch
git push -u origin master
```

## Step 5: Create GitHub Repository (if not done)

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `353-aromatic`
4. Description: "Phylogenomic analysis pipeline for aromatic plants using 353 nuclear genes"
5. Public/Private: Choose based on your needs
6. Check "Add a README file"
7. Click "Create repository"

## Recommended Repository Structure

```
353-aromatic/
├── .gitignore              # Ignore large files
├── README.md               # Project overview
├── LICENSE                 # MIT License
├── requirements.txt        # Python dependencies
├── environment.yml         # Conda environment
├── config/
│   ├── parameters.yaml     # Analysis parameters
│   └── input_list.txt      # Input data list (small example)
├── scripts/                # Analysis scripts
│   ├── run_pipeline.py
│   ├── 01_data_preprocessing.py
│   ├── 02_alignment.py
│   ├── 03_gene_tree_inference.py
│   ├── 04_concatenation.py
│   ├── 05_coalescent.py
│   └── 06_result_integration.py
├── docs/                   # Documentation
│   ├── getting_started.md
│   ├── parameter_guide.md
│   └── workflow_diagram.md
└── data/                   # NOT included in repo (see .gitignore)
    └── sequences/          # Your sequence data
```

## Best Practices

### 1. Keep Large Files Out of Repository

- **DO NOT commit**: Sequence files, alignment files, tree files
- **DO commit**: Scripts, documentation, configuration files
- Use `.gitignore` to exclude large files

### 2. Document Everything

- Update README with your specific details
- Add comments to scripts
- Document parameters and options

### 3. Version Control

- Use meaningful commit messages
- Create branches for new features
- Tag releases when publishing

```bash
# Create branch for new feature
git checkout -b feature/new-analysis

# Make changes, commit, then merge
git add .
git commit -m "Add new analysis method"
git checkout main
git merge feature/new-analysis

# Tag a release
git tag -a v1.0 -m "Version 1.0: Initial release"
git push origin v1.0
```

### 4. Use Releases

When your paper is published:

```bash
# Create release on GitHub
git tag -a v1.0-paper -m "Version used in publication"
git push origin v1.0-paper
```

## GitHub Features to Use

### 1. Issues

Use issues for:
- Bug reports
- Feature requests
- Questions

### 2. Projects

Create a project board to track:
- Tasks
- Milestones
- Paper writing progress

### 3. Actions

Set up GitHub Actions for:
- Automated testing
- Code quality checks

## Citation File

Create a `CITATION.cff` file for citations:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "YourLastName"
    given-names: "YourFirstName"
title: "353 Phylogenomics Pipeline"
version: 1.0
date-released: 2026-04-23
url: "https://github.com/tongyinplant123/353-aromatic"
```

## License

This repository uses the MIT License (see LICENSE file).

## Contact

Add your contact information to README.md:

```markdown
## Contact

For questions or issues, please open an issue on GitHub or contact:
[Your Name] - your.email@domain.com
```

## Acknowledgments

Add funding information:

```markdown
## Acknowledgments

This work was supported by [Funding Agency] under grant [Number].
```

## Next Steps

1. ✅ Set up GitHub repository
2. ✅ Add documentation
3. ✅ Test with sample data
4. ✅ Add your actual data (locally, not in repo)
5. ✅ Run full analysis
6. ✅ Publish paper and tag release

## Troubleshooting

### Issue: "Permission denied" when pushing

**Solution**: Check your SSH keys or use HTTPS with credentials

### Issue: "Repository not found"

**Solution**: Verify remote URL
```bash
git remote -v
```

### Issue: Large files still being committed

**Solution**: Check `.gitignore` and use `git rm --cached` for already committed files

```bash
git rm --cached data/sequences/*
git commit -m "Remove large files from repository"
```

## Resources

- [GitHub Docs](https://docs.github.com)
- [Git Book](https://git-scm.com/book/en/v2)
- [GitHub Learning Lab](https://lab.github.com)
