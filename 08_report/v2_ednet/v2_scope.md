# V2 EdNet Real Dataset Scope

## Purpose

V2 extends the synthetic V1 prototype to real educational interaction data using EdNet.

The goal is not to process the full EdNet dataset. Instead, this phase uses a controlled EdNet subset to test whether the existing adaptive tutor pipeline can work with real student-question interactions.

## Main Goal

The main goal of V2 is to compare model behavior across:

- V1 synthetic student interaction data
- V2 real EdNet student interaction data

This makes the project stronger because it moves from architecture proof-of-concept to real-data validation.

## Planned Scope

The planned V2 subset target is:

- Dataset: EdNet
- Students: around 10,000
- Interactions: around 500,000
- Minimum interactions per student: 20
- Main task: correctness prediction
- Main model type: supervised learning baseline models

## Included in V2

V2 will include:

- EdNet dataset preparation
- Column mapping into the project format
- Real-data feature engineering
- Supervised model training
- Synthetic V1 vs EdNet V2 comparison
- Basic error analysis
- Updated research summary

## Excluded from V2

To keep the project controlled, V2 will not include:

- Full EdNet scale processing
- Deep Knowledge Tracing models
- Real reinforcement learning deployment
- Advanced recommender system training
- Live visitor testing on the website

## Expected Outcome

The expected outcome is a real-data validation layer that shows whether the project pipeline can generalize beyond synthetic data.

V1 proves the architecture.

V2 tests the architecture on real educational interaction data.