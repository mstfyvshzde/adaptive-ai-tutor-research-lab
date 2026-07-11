# Data Directory

This folder contains the data used by the Adaptive AI Tutor Research Lab.

## Structure

- `raw/` stores original raw data.
- `interim/` stores partially processed data.
- `processed/` stores model-ready datasets.
- `external/` is reserved for future real educational datasets.
- `data_dictionary.md` explains the main dataset columns.
- `dataset_decision.md` explains why the current version uses synthetic data.

## Current Data

The current project version uses synthetic student interaction data.

The synthetic data includes:

- students
- questions
- topic tags
- difficulty levels
- elapsed time
- correctness labels

Synthetic data is used because it makes the project reproducible and avoids privacy risks during early development.

## Future Data

Future versions can extend this project with real educational datasets such as ASSISTments or EdNet.