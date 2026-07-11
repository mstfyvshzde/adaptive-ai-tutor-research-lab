# System Architecture

## 1. Overview

This document explains the system architecture of the Adaptive AI Tutor Research Lab.

The project is designed as a modular AI/ML research pipeline.

Main flow:

data → validation → features → models → recommendations → reinforcement learning → evaluation → visualization → demo

## 2. Main Architecture Layers

The project has several layers:

1. Data layer
2. Feature engineering layer
3. Modeling layer
4. Recommendation layer
5. Reinforcement learning layer
6. Evaluation layer
7. Visualization layer
8. Demo layer
9. Documentation layer

## 3. Data Layer

The data layer creates and stores student interaction data.

Main files:

- `04_src/data/create_demo_dataset.py`
- `04_src/data/validate_demo_dataset.py`

Main outputs:

- `07_demo/demo_data/demo_questions.csv`
- `07_demo/demo_data/demo_interactions.csv`

The current version uses synthetic data for privacy and reproducibility.

## 4. Feature Engineering Layer

The feature layer converts raw interactions into model-ready data.

Main file:

- `04_src/features/build_features.py`

Main output:

- `02_data/processed/demo_features.csv`

Feature examples:

- student accuracy so far
- previous correctness
- rolling accuracy
- topic-level accuracy
- question-level accuracy
- elapsed time
- difficulty score

## 5. Modeling Layer

The modeling layer trains and evaluates machine learning models.

Main files:

- `04_src/models/supervised_baselines.py`
- `04_src/models/clustering.py`
- `04_src/models/recommender.py`

Main tasks:

- predict answer correctness
- group students by learning behavior
- create recommendation examples

## 6. Recommendation Layer

The recommendation layer suggests learning activities.

Current recommendation strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

The goal is to move from prediction to action.

## 7. Reinforcement Learning Layer

The reinforcement learning layer simulates an adaptive tutor.

Main files:

- `04_src/rl/environment.py`
- `04_src/rl/q_learning_agent.py`

The tutor observes a state, chooses an action, receives a reward, and learns better decisions over time.

State examples:

- recent accuracy
- weak topic
- current step

Actions:

- easy question
- medium question
- hard question

## 8. Evaluation Layer

The evaluation layer compares different models and policies.

Main file:

- `04_src/evaluation/compare_rl_policies.py`

Evaluation examples:

- supervised model metrics
- clustering silhouette score
- random policy vs Q-learning policy

## 9. Visualization Layer

The visualization layer creates plots from results.

Main files:

- `04_src/visualization/plot_supervised_results.py`
- `04_src/visualization/plot_rl_results.py`

Main outputs:

- supervised model comparison plots
- clustering plot
- Q-learning reward curve
- RL policy comparison plot

## 10. Demo Layer

The demo layer presents the project visually.

Main file:

- `07_demo/app.py`

The demo shows:

- dataset overview
- supervised model results
- student clustering
- recommendation examples
- reinforcement learning comparison

## 11. Pipeline Runner

The full pipeline is controlled by:

- `run_pipeline.py`

Main command:

`python run_pipeline.py`

This command runs the full project from data generation to visualization.

## 12. Testing Layer

The testing layer checks whether the full pipeline works.

Main file:

- `tests/test_pipeline_smoke.py`

Main command:

`pytest`

The test runs the full pipeline and checks expected output files.

## 13. Summary

The project architecture is designed to be modular and reproducible.

Each component has a clear role, and the full system can be run with one command.