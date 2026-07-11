# Contributing

## Overview

Thank you for your interest in the Adaptive AI Tutor Research Lab.

This project is a research-style AI/ML prototype for adaptive learning. It includes data generation, feature engineering, supervised learning, clustering, recommendation strategies, reinforcement learning simulation, evaluation, visualization, testing, documentation, and a Streamlit demo.

## Development Setup

Recommended setup:

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run the full pipeline.
5. Run tests.

Main commands:

`python run_pipeline.py`

`pytest`

`streamlit run 07_demo/app.py`

## Before Making Changes

Before changing the project, please understand the main pipeline:

data generation → validation → feature engineering → supervised learning → clustering → recommendation → reinforcement learning → evaluation → visualization → demo

The main pipeline is controlled by:

`run_pipeline.py`

## Code Guidelines

Please keep code:

- clear
- modular
- readable
- documented with simple docstrings
- reproducible where possible

Avoid adding unnecessary complexity unless it improves the research value of the project.

## Testing

After making changes, run:

`python run_pipeline.py`

`pytest`

A successful test should show that the full pipeline runs and expected outputs are created.

## Documentation

When adding a new feature, update relevant documentation.

Useful documentation folders:

- `10_docs/`
- `08_report/`
- `09_portfolio_assets/`

## Data Guidelines

The current project uses synthetic data.

Large real datasets should not be committed directly to the repository unless the license clearly allows it.

For real datasets, prefer documenting download instructions and preprocessing steps.

## Pull Request Checklist

Before submitting changes, check:

- the pipeline runs successfully
- tests pass
- new files are documented
- no unnecessary large files are committed
- results are reproducible
- limitations are clearly explained

## Summary

The goal of this project is not only to build models, but to build a clear, reproducible, and responsible AI/ML research prototype.