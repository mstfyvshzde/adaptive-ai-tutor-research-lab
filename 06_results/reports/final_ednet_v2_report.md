# Adaptive AI Tutor Research Lab  
## V2 Real-Data Validation with EdNet

## 1. Project Overview

This project explores an adaptive AI tutoring system using student interaction data, knowledge tracing-inspired features, supervised learning models, and experimental evaluation.

The project started with a synthetic prototype and was later extended to real educational data using the EdNet KT1 dataset.

The main prediction task is:

**Predict whether a student will answer a question correctly based on previous learning interactions.**

This is framed as a binary classification problem:

- `1`: student answered correctly
- `0`: student answered incorrectly

## 2. Motivation

Adaptive tutoring systems need to estimate student knowledge in order to personalize learning.

If a system can predict whether a student is likely to answer a question correctly, it can recommend better next questions, detect struggling students, and support personalized learning paths.

The goal of this project is not to claim a new algorithm, but to build a clean and realistic applied machine learning research pipeline for educational data mining.

## 3. Dataset

The real-data validation uses the EdNet KT1 dataset.

### EdNet KT1 Scope

- Student interaction files from KT1
- Question metadata from `contents/questions.csv`
- Raw data is kept local and not committed to GitHub

### Main Columns

Student interaction files include:

- `timestamp`
- `solving_id`
- `question_id`
- `user_answer`
- `elapsed_time`

Question metadata includes:

- `question_id`
- `correct_answer`
- `part`
- `tags`

Correctness is computed as:

`is_correct = user_answer == correct_answer`

## 4. Methodology

The project uses a leakage-free feature engineering pipeline.

All history-based features are computed using only previous interactions.

The current row's correctness is not used when creating features for that same row.

This is important because using current correctness during feature creation would produce unrealistic performance.

## 5. Models

The supervised learning models include:

- Dummy Majority Baseline
- Logistic Regression
- Random Forest
- Gradient Boosting
- Histogram Gradient Boosting

The main evaluation metric is:

- ROC-AUC

Secondary metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- Log Loss

A time-based split is used to better simulate future prediction.

## 6. Scale Experiments

| Stage | Data Source | Interactions | Best Model | ROC-AUC |
|---|---|---:|---|---:|
| V1 Synthetic | Synthetic prototype data | 1,452 | Logistic Regression | 0.9077 |
| EdNet 5k | Real EdNet KT1 | 5,017 | Gradient Boosting | 0.6250 |
| EdNet 50k | Real EdNet KT1 | 50,081 | Gradient Boosting | 0.7080 |
| EdNet 200k | Real EdNet KT1 | 200,091 | Gradient Boosting | 0.7222 |
| EdNet 500k Final | Real EdNet KT1 | 500,057 | Gradient Boosting | 0.7301 |

The results show that model performance improved as the real EdNet subset size increased.

This suggests that the prediction pipeline benefits from larger student interaction histories.

## 7. Feature Ablation

| Feature Set | Best Model | Accuracy | F1 | ROC-AUC | Log Loss |
|---|---|---:|---:|---:|---:|
| Baseline Features | Gradient Boosting | 0.6799 | 0.7523 | 0.7301 | 0.5939 |
| Enhanced Features | Random Forest | 0.6771 | 0.7557 | 0.7298 | 0.5956 |

The enhanced feature set achieved comparable performance but did not produce a meaningful ROC-AUC improvement.

This suggests that the baseline history-based features were already strong for this task.

## 8. Feature Importance

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | `ability_minus_difficulty` | 0.1761 |
| 2 | `recent_accuracy_minus_difficulty` | 0.1274 |
| 3 | `question_difficulty_estimate` | 0.1233 |
| 4 | `question_accuracy_so_far` | 0.1130 |
| 5 | `elapsed_time_ratio_vs_question_avg` | 0.0436 |

The strongest predictive signals are related to the relationship between student ability and question difficulty.

This supports the educational interpretation that correctness prediction depends heavily on whether the question difficulty matches the student's current performance level.

## 9. Error Analysis

### Student History

| Student History | Error Rate |
|---|---:|
| 0-4 attempts | 35.5% |
| 5-19 attempts | 33.9% |
| 20-49 attempts | 32.1% |
| 50-99 attempts | 32.4% |
| 100+ attempts | 30.9% |

The model became more reliable when more student interaction history was available.

### Question Difficulty

| Difficulty Group | Error Rate |
|---|---:|
| Easy | 22.4% |
| Medium | 36.6% |
| Hard | 37.4% |
| Very Hard | 28.9% |

The model made more errors on harder question groups, which is expected in educational prediction tasks.

### Model Confidence

| Confidence Group | Error Rate |
|---|---:|
| Low | 44.8% |
| Medium | 32.4% |
| High | 17.5% |
| Very High | 6.1% |

The model's confidence was strongly related to prediction accuracy.

This suggests that model confidence could be used by an adaptive tutor to decide when predictions are reliable.

## 10. Limitations

This project has several limitations:

- It does not introduce a new algorithm.
- It does not yet include deep knowledge tracing models.
- It does not compare against DKT, SAKT, or Transformer-based KT.
- Some probability estimates appear overconfident.
- The current analysis focuses on classic ML baselines.

For example, in the medium difficulty group, actual correctness was around `0.605`, while predicted correctness was around `0.818`.

This suggests that future work should include probability calibration.

## 11. Future Work

Future improvements could include:

- Deep Knowledge Tracing
- SAKT
- Transformer-based Knowledge Tracing
- Probability calibration
- Student cold-start analysis
- Question cold-start analysis
- More detailed tag-level performance analysis
- Personalized recommendation experiments

## 12. Conclusion

This project successfully extends a synthetic adaptive tutor prototype into a real-data educational machine learning pipeline using EdNet.

The strongest real-data result achieved ROC-AUC `0.7301` on `500,057` student interactions.

The project includes:

- real educational dataset validation
- leakage-free feature engineering
- supervised model comparison
- scale experiments
- feature ablation
- feature importance
- error analysis

This project is best described as a strong applied machine learning research portfolio project in educational data mining.
