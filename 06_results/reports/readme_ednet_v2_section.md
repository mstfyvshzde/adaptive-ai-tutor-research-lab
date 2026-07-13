## V2: Real-Data Validation with EdNet

This project was extended from a synthetic adaptive tutor prototype to a real educational data validation pipeline using the EdNet KT1 dataset.

The main task is **student correctness prediction**: predicting whether a student will answer a question correctly based on previous interaction history and question-level signals.

### Dataset

- Dataset: EdNet KT1
- Raw data: local only, not committed to GitHub
- Scope: KT1 student interaction files + `contents/questions.csv`
- Target: `is_correct = user_answer == correct_answer`

### Main Results

| Stage | Data Source | Interactions | Best Model | ROC-AUC |
|---|---|---:|---|---:|
| V1 Synthetic | Synthetic prototype data | 1,452 | Logistic Regression | 0.9077 |
| EdNet 5k | Real EdNet KT1 | 5,017 | Gradient Boosting | 0.6250 |
| EdNet 50k | Real EdNet KT1 | 50,081 | Gradient Boosting | 0.7080 |
| EdNet 200k | Real EdNet KT1 | 200,091 | Gradient Boosting | 0.7222 |
| EdNet 500k Final | Real EdNet KT1 | 500,057 | Gradient Boosting | 0.7301 |

The results show that model performance improved as the real EdNet subset size increased, suggesting that the pipeline benefits from larger student interaction histories.

### Feature Ablation

| Feature Set | Best Model | ROC-AUC | Log Loss |
|---|---|---:|---:|
| Baseline Features | Gradient Boosting | 0.7301 | 0.5939 |
| Enhanced Features | Random Forest | 0.7298 | 0.5956 |

Additional leakage-free feature engineering achieved comparable performance but did not materially improve ROC-AUC. This suggests that the baseline history-based features were already strong for this task.

### Feature Importance

The strongest predictive signals were:

1. `ability_minus_difficulty`
2. `recent_accuracy_minus_difficulty`
3. `question_difficulty_estimate`
4. `question_accuracy_so_far`
5. `elapsed_time_ratio_vs_question_avg`

This supports the educational interpretation that correctness prediction depends strongly on the match between a student's recent performance and the estimated difficulty of the question.

### Error Analysis

The model became more reliable when more student history was available:

| Student History | Error Rate |
|---|---:|
| 0-4 attempts | 35.5% |
| 5-19 attempts | 33.9% |
| 20-49 attempts | 32.1% |
| 50-99 attempts | 32.4% |
| 100+ attempts | 30.9% |

Model confidence was also strongly related to accuracy:

| Confidence Group | Error Rate |
|---|---:|
| Low | 44.8% |
| Medium | 32.4% |
| High | 17.5% |
| Very High | 6.1% |

### Research Summary

This project is best described as a **strong applied machine learning research portfolio project** in educational data mining.

It includes:

- real educational dataset validation
- leakage-free feature engineering
- supervised ML baselines
- scale experiments
- ablation analysis
- feature importance
- error analysis

Future work could extend the project with Deep Knowledge Tracing, SAKT, Transformer-based KT, probability calibration, and student/question cold-start experiments.
