# Processed EdNet Data

This folder stores processed EdNet V2 files created by the preprocessing pipeline.

## Main Files

Expected generated files:

- `ednet_interactions_mapped.csv`
- `ednet_subset_metadata.json`
- `ednet_features.csv`

## Important Note

Processed EdNet files may be large and should not always be committed to GitHub.

The repository should mainly include:

- preprocessing scripts
- validation scripts
- experiment configuration
- result summaries
- documentation

## How to Recreate

After placing raw EdNet files inside:

`02_data/external/ednet/`

run:

`python 04_src/data/prepare_ednet_subset.py`

Then validate the generated dataset:

`python 04_src/data/validate_ednet_dataset.py`

## Purpose

These processed files are used for V2 real-dataset validation.

V1 used synthetic data.

V2 uses real EdNet interaction data to test whether the adaptive tutor pipeline can generalize beyond synthetic examples.