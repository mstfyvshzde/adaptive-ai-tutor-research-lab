# Ablation Plan

## 1. Overview

This document describes possible ablation experiments for the Adaptive AI Tutor Research Lab.

Ablation means removing or changing one part of the system to understand how important it is.

## 2. Why Ablation Matters

A machine learning project should not only show final results.

It should also investigate which components are actually useful.

Ablation helps answer questions such as:

- Which features matter most?
- Does topic history improve prediction?
- Does rolling accuracy help?
- Does difficulty information improve results?
- Does Q-learning perform better than random policy because it actually learns?

## 3. Feature Ablation

The supervised model uses several feature groups.

Possible ablation experiments:

1. Remove rolling accuracy features.
2. Remove topic-level accuracy features.
3. Remove question-level accuracy features.
4. Remove elapsed time features.
5. Remove difficulty features.
6. Train only with basic student history features.
7. Train only with question and topic features.

The goal is to compare model performance after removing each feature group.

## 4. Model Ablation

The project compares multiple supervised models.

Possible model ablations:

- Dummy Classifier only
- Logistic Regression only
- Random Forest only
- Gradient Boosting only

This helps understand whether simpler models are enough or more complex models add value.

## 5. Recommendation Ablation

The recommendation system has three strategies.

Possible ablations:

1. Use only random recommendation.
2. Use only difficulty-based recommendation.
3. Use only weak-topic recommendation.
4. Compare recommendation strategies across student groups.

The goal is to understand which recommendation logic is more useful.

## 6. Reinforcement Learning Ablation

The reinforcement learning system can be analyzed by changing reward design and policy type.

Possible ablations:

1. Remove weak-topic reward bonus.
2. Remove too-easy penalty.
3. Remove too-hard penalty.
4. Compare random policy with Q-learning.
5. Test different epsilon values.
6. Test different episode counts.

The goal is to see whether the RL tutor still performs well under different assumptions.

## 7. Clustering Ablation

The clustering system can be tested with different student-level features.

Possible ablations:

1. Remove accuracy change.
2. Remove topic diversity.
3. Remove elapsed time.
4. Change number of clusters.
5. Compare silhouette scores.

The goal is to check whether clusters are meaningful or sensitive to feature choices.

## 8. Expected Outputs

Future ablation experiments can produce:

- comparison tables
- feature group importance summaries
- updated supervised metrics
- updated RL policy comparisons
- updated plots
- analysis notes

## 9. Current Status

The current project does not yet run automated ablation experiments.

This document is a research plan for future improvement.

## 10. Summary

Ablation experiments would make the project more research-ready.

They would help show which parts of the adaptive tutor pipeline are actually responsible for performance improvements.