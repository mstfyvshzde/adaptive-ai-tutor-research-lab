# Experiment Plan

## Purpose

This document defines the first experiment plan for the Adaptive AI Tutor Research Lab.

The goal is to build the project step by step, starting from simple baselines and moving toward reinforcement learning.

This project is not only a software project. It is an AI + education + learning science research project.

## Main Research Question

Can a reinforcement learning-based tutoring policy improve personalized learning paths compared to random, difficulty-based, supervised, and recommender-based baselines?

## Experiment Strategy

The project will not start with the most complex model.

The first goal is to build a clean and reproducible pipeline.

The experiment order will be:

1. Data exploration
2. Data preprocessing
3. Supervised knowledge tracing
4. Student behavior clustering
5. Recommender baselines
6. Reinforcement learning environment
7. RL policy comparison
8. Ablation study
9. Final evaluation

## Experiment 1 — Dataset Exploration

### Goal

Understand the structure and quality of the dataset.

### Tasks

- Load a small sample of EdNet-KT1
- Inspect columns
- Check missing values
- Analyze student activity
- Analyze question frequency
- Analyze elapsed time
- Analyze correctness distribution

### Output

- Dataset summary
- Initial visualizations
- Data quality notes

## Experiment 2 — Data Preprocessing

### Goal

Create a clean dataset for modeling.

### Tasks

- Extract user IDs
- Join interaction logs with question metadata
- Create `is_correct` target
- Sort interactions by timestamp
- Filter low-activity students
- Filter low-frequency questions
- Save processed dataset

### Output

- Clean processed dataset
- Data dictionary update
- Preprocessing notes

## Experiment 3 — Supervised Knowledge Tracing

### Goal

Predict whether a student will answer a question correctly.

### Models

- Majority-class baseline
- Logistic Regression
- Random Forest
- Gradient Boosting

### Metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Log Loss

### Output

- Model comparison table
- Feature importance
- Supervised learning results

## Experiment 4 — Student Behavior Clustering

### Goal

Group students based on learning behavior.

### Features

- Average accuracy
- Recent accuracy
- Average elapsed time
- Attempt count
- Improvement rate
- Topic diversity

### Models

- K-Means
- Gaussian Mixture Model

### Output

- Cluster visualization
- Student group interpretation
- Cluster summary table

## Experiment 5 — Recommender Baselines

### Goal

Build simple recommendation strategies before reinforcement learning.

### Baselines

- Random recommendation
- Difficulty-based recommendation
- Weak-topic recommendation
- Content-based recommendation
- Supervised model-based recommendation

### Output

- Baseline comparison table
- Recommendation examples
- Recommendation explanation notes

## Experiment 6 — Reinforcement Learning Environment

### Goal

Design a tutoring environment for sequential decision-making.

### State

Possible state features:

- Student recent accuracy
- Topic mastery
- Attempt count
- Current difficulty
- Weak-topic signal
- Student cluster

### Action

Possible actions:

- Recommend easy question
- Recommend medium question
- Recommend hard question
- Review weak topic
- Continue current topic
- Switch topic

### Reward

Possible reward signals:

- Correct answer
- Mastery improvement
- Weak-topic improvement
- Penalty for too easy questions
- Penalty for too difficult questions

### Output

- RL environment design
- Random policy test
- Reward function notes

## Experiment 7 — RL Policy Training

### Goal

Compare reinforcement learning policies against baseline recommendation methods.

### Methods

- Random policy
- Bandit policy
- Q-learning policy

### Metrics

- Cumulative reward
- Average reward per episode
- Learning gain
- Mastery improvement
- Policy comparison

### Output

- Reward curves
- Policy comparison table
- RL analysis notes

## Experiment 8 — Ablation Study

### Goal

Understand which system components matter most.

### Ablation Tests

- Without student history
- Without question difficulty
- Without weak-topic signal
- Without clustering features
- Without reward shaping

### Output

- Ablation results table
- Component importance analysis
- Limitations notes

## Final Evaluation

The final evaluation will compare all major methods:

- Random baseline
- Difficulty-based baseline
- Weak-topic recommender
- Supervised recommender
- RL-based tutor policy

The goal is to understand whether reinforcement learning improves personalized learning decisions compared to simpler methods.

## Expected Final Outputs

- Clean experiment notebooks
- Saved metrics
- Saved figures
- Model comparison table
- Baseline comparison table
- RL reward curves
- Ablation study
- Final research report
- Demo application
