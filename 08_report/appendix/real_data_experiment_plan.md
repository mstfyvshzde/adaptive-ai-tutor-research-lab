# Real Data Experiment Plan

## 1. Overview

This document describes a future experiment for testing the Adaptive AI Tutor Research Lab on a real educational dataset.

The current version is a synthetic prototype.

The next research phase is to evaluate the pipeline with real student interaction data.

## 2. Experiment Goal

The goal is to test whether the existing adaptive tutor pipeline can work with real educational data.

Main question:

Can the pipeline built on synthetic data be adapted to real student interaction data?

## 3. Dataset Choice

Candidate datasets:

- ASSISTments
- EdNet
- KDD Cup educational datasets

The first selected dataset should be manageable, well-documented, and suitable for knowledge tracing.

## 4. Data Preparation

The real dataset should be cleaned and transformed into the project format.

Target columns:

- student_id
- question_id
- timestamp
- tags
- difficulty
- elapsed_time
- is_correct

If some columns are missing, the experiment should document how they were handled.

## 5. Experiment Steps

Planned steps:

1. Select dataset.
2. Download dataset.
3. Inspect columns.
4. Create data mapping.
5. Clean missing or invalid rows.
6. Create project-format interaction file.
7. Build features.
8. Train supervised baselines.
9. Run clustering.
10. Test recommendation strategies.
11. Compare results with synthetic prototype.
12. Document limitations.

## 6. Evaluation

The real data experiment should evaluate:

- supervised prediction performance
- feature usefulness
- cluster quality
- recommendation interpretability
- data quality issues
- pipeline stability

Possible metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Log Loss
- Silhouette Score

## 7. Comparison With Synthetic Data

The real data results should be compared with synthetic data results.

Important questions:

- Are model scores lower or higher on real data?
- Are some features less useful on real data?
- Do student clusters become more meaningful?
- Are topic-based recommendations more realistic?
- Does the pipeline require major changes?

## 8. Expected Challenges

Possible challenges:

- messy real-world columns
- missing timestamps
- missing response time
- inconsistent skill tags
- very large data size
- multiple attempts per question
- students with very few interactions
- dataset license restrictions

## 9. Success Criteria

The experiment is successful if:

- real data can be loaded
- the dataset can be mapped into project format
- feature engineering runs
- supervised models train successfully
- results can be compared with synthetic version
- limitations are clearly documented

## 10. Summary

This experiment is the bridge between the current portfolio prototype and a stronger research-level project.

The synthetic version proves the architecture.

The real data experiment tests whether the architecture can handle real educational data.