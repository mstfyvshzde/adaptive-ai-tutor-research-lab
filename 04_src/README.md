# Source Code Directory

This folder contains the main Python source code for the Adaptive AI Tutor Research Lab.

## Structure

- `data/` contains scripts for creating and validating the demo dataset.
- `features/` contains feature engineering code.
- `models/` contains supervised learning, clustering, and recommendation scripts.
- `rl/` contains reinforcement learning environment and Q-learning agent code.
- `evaluation/` contains comparison and evaluation scripts.
- `visualization/` contains plotting scripts.

## Main Flow

The source code follows this order:

1. Create demo data
2. Validate data
3. Build features
4. Train supervised models
5. Run clustering
6. Generate recommendations
7. Run reinforcement learning simulation
8. Compare policies
9. Create visualizations

The full flow can be executed from the project root with:

`python run_pipeline.py`

## Purpose

This folder is the technical engine of the project.

It turns the project idea into a working machine learning pipeline.