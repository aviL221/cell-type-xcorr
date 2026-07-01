# template_project

## Overview

Template directory for a research project

## Setup

```bash
mamba env create -f environment.yml
conda activate my_project
pip install -e .
```

## Project layout

```
├── src/my_project/     # importable package code
├── scripts/            # standalone scripts (e.g. run_analysis.py)
├── notebooks/          # exploratory notebooks
├── data/               # data files (see data/README.md)
└── tests/              # unit tests
```

## Usage

```bash
python scripts/run_analysis.py
```
