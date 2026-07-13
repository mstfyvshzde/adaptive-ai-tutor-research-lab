# Final Research Insights - EdNet V2

## Main Result

The project successfully moved from a synthetic prototype to real educational data validation using the EdNet KT1 dataset.

The best real-data result was achieved on the 500k interaction subset:

- Dataset: EdNet KT1
- Interactions: 500,057
- Best model: Gradient Boosting
- ROC-AUC: 0.7301

Model performance improved as the real EdNet subset size increased:

| Scale | Interactions | ROC-AUC |
|---|---:|---:|
| EdNet 5k | 5,017 | 0.6250 |
| EdNet 50k | 50,081 | 0.7080 |
| EdNet 200k | 200,091 | 0.7222 |
| EdNet 500k | 500,057 | 0.7301 |

This suggests that the pipeline benefits from larger student interaction histories.

## Ablation Finding

A leakage-free enhanced feature set was tested against the baseline feature set.

| Feature Set | Best Model | ROC-AUC |
|---|---|---:|
| Baseline Features | Gradient Boosting | 0.7301 |
| Enhanced Features | Random Forest | 0.7298 |

The enhanced feature set achieved comparable performance but did not provide a meaningful ROC-AUC improvement. This suggests that the baseline history-based features were already strong for the EdNet correctness prediction task.

## Feature Importance

The most important predictive signals were related to the relationship between student ability and question difficulty:

1. ability_minus_difficulty
2. recent_accuracy_minus_difficulty
3. question_difficulty_estimate
4. question_accuracy_so_far
5. elapsed_time_ratio_vs_question_avg

This supports the educational interpretation that correctness prediction depends strongly on the match between a student's recent performance and the estimated difficulty of the question.

## Error Analysis

The model showed better performance when it had more student history.

| Student History | Error Rate |
|---|---:|
| 0-4 attempts | 35.5% |
| 5-19 attempts | 33.9% |
| 20-49 attempts | 32.1% |
| 50-99 attempts | 32.4% |
| 100+ attempts | 30.9% |

This supports the idea that adaptive tutoring systems become more reliable as they observe more student interactions.

The model also made more errors on harder question groups:

| Difficulty Group | Error Rate |
|---|---:|
| Easy | 22.4% |
| Medium | 36.6% |
| Hard | 37.4% |
| Very Hard | 28.9% |

Model confidence was strongly related to prediction accuracy:

| Confidence Group | Error Rate |
|---|---:|
| Low | 44.8% |
| Medium | 32.4% |
| High | 17.5% |
| Very High | 6.1% |

This suggests that model confidence can be useful for deciding when an AI tutor should trust its prediction or request more information.

## Limitation

The model sometimes overestimated correctness in certain groups. For example, in the medium difficulty group, actual correctness was 0.605 while predicted correctness was 0.818.

This suggests that future work should consider probability calibration and stronger knowledge tracing models such as DKT, SAKT, or Transformer-based KT.

## Final Interpretation

Overall, this project provides a strong applied machine learning research pipeline for educational data mining. It includes real-data validation, leakage-free feature engineering, supervised baselines, scale experiments, ablation analysis, feature importance, and error analysis.

The project is best described as a strong applied ML research portfolio project rather than a novel algorithmic research paper.
