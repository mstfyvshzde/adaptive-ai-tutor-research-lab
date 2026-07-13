# Adaptive AI Tutor Research Lab  
## Academic-Style Final Research Report Outline

Target length: 40-60 pages  
Project type: Applied Machine Learning Research Portfolio Project  
Domain: Educational Data Mining / Adaptive Learning / Knowledge Tracing

---

## Front Matter

### Title Page
- Project title
- Author
- GitHub repository
- Version: v2.0-ednet
- Date

Estimated length: 1 page

### Abstract
- Short summary of the problem
- Dataset
- Methodology
- Main results
- Key conclusion

Estimated length: 0.5-1 page

### Table of Contents
Estimated length: 1 page

---

## 1. Introduction

### 1.1 Project Motivation
Explain why adaptive tutoring systems matter.

### 1.2 Problem Statement
Define student correctness prediction.

### 1.3 Research Questions
Possible research questions:
- Can student correctness be predicted from interaction history?
- Does real-data scale improve model performance?
- Which features are most predictive?
- Where does the model make more errors?

### 1.4 Project Contributions
Main contributions:
- End-to-end adaptive tutor prototype
- Real-data validation on EdNet KT1
- Leakage-aware feature engineering
- Scale experiments
- Ablation analysis
- Feature importance
- Error analysis

Estimated length: 4-5 pages

---

## 2. Background and Related Work

### 2.1 Intelligent Tutoring Systems
Brief overview of AI tutoring systems.

### 2.2 Educational Data Mining
Explain how student interaction data is used.

### 2.3 Knowledge Tracing
Cover:
- Bayesian Knowledge Tracing
- Deep Knowledge Tracing
- Attention-based Knowledge Tracing
- Transformer-based Knowledge Tracing

### 2.4 EdNet Dataset
Explain why EdNet is useful for educational ML.

### 2.5 Research Gap
Position this project as an applied ML validation pipeline rather than a new algorithm paper.

Estimated length: 6-8 pages

---

## 3. Dataset

### 3.1 Synthetic V1 Dataset
Explain synthetic prototype data.

### 3.2 EdNet KT1 Dataset
Explain:
- KT1 student interaction files
- question metadata
- correctness calculation

### 3.3 Data Scope
Explain local-only raw data policy.

### 3.4 Data Preparation
Explain subset construction:
- 5k
- 50k
- 200k
- 500k

### 3.5 Data Validation
Include validation summary:
- students
- questions
- interactions
- average correctness

Estimated length: 5-6 pages

---

## 4. Methodology

### 4.1 Overall Pipeline
Show pipeline:
data validation → feature engineering → modeling → evaluation → analysis

### 4.2 Leakage-Aware Design
Explain why current-row correctness must not be used as a feature.

### 4.3 Time-Based Split
Explain why time-based split is more realistic than random split.

### 4.4 Evaluation Metrics
Explain:
- ROC-AUC
- Accuracy
- Precision
- Recall
- F1
- Log Loss

Estimated length: 5-6 pages

---

## 5. Feature Engineering

### 5.1 Baseline Features
Explain:
- student accuracy so far
- question accuracy so far
- elapsed time
- difficulty estimates

### 5.2 Enhanced Features
Explain:
- rolling accuracy
- streaks
- activity gaps
- elapsed time ratios
- ability-minus-difficulty features

### 5.3 Leakage Prevention
Explain cumsum-minus-current, shift, and history-only computation.

### 5.4 Feature Summary
Include feature table.

Estimated length: 5-6 pages

---

## 6. Models

### 6.1 Dummy Majority Baseline
### 6.2 Logistic Regression
### 6.3 Random Forest
### 6.4 Gradient Boosting
### 6.5 Histogram Gradient Boosting

For each model:
- why it was included
- strengths
- limitations

Estimated length: 4-5 pages

---

## 7. Experiments

### 7.1 V1 Synthetic Experiment
Include V1 synthetic result.

### 7.2 EdNet 5k Pilot
### 7.3 EdNet 50k Small
### 7.4 EdNet 200k Medium
### 7.5 EdNet 500k Final

### 7.6 Experimental Setup
Explain config:
- target students
- target interactions
- min/max interactions per student

Estimated length: 5-6 pages

---

## 8. Results

### 8.1 Main V1 vs V2 Comparison

Main table:

| Stage | Data Source | Interactions | Best Model | ROC-AUC |
|---|---|---:|---|---:|
| V1 Synthetic | Synthetic prototype data | 1,452 | Logistic Regression | 0.9077 |
| EdNet 5k | Real EdNet KT1 | 5,017 | Gradient Boosting | 0.6250 |
| EdNet 50k | Real EdNet KT1 | 50,081 | Gradient Boosting | 0.7080 |
| EdNet 200k | Real EdNet KT1 | 200,091 | Gradient Boosting | 0.7222 |
| EdNet 500k Final | Real EdNet KT1 | 500,057 | Gradient Boosting | 0.7301 |

### 8.2 Scale Trend Interpretation
Explain why performance improves with more interactions.

### 8.3 Real-Data vs Synthetic Performance
Explain why synthetic score is higher and real-data score is more realistic.

Estimated length: 4-5 pages

---

## 9. Ablation Study

### 9.1 Motivation
Explain why enhanced features were tested.

### 9.2 Baseline vs Enhanced Results

| Feature Set | Best Model | Accuracy | F1 | ROC-AUC | Log Loss |
|---|---|---:|---:|---:|---:|
| Baseline Features | Gradient Boosting | 0.6799 | 0.7523 | 0.7301 | 0.5939 |
| Enhanced Features | Random Forest | 0.6771 | 0.7557 | 0.7298 | 0.5956 |

### 9.3 Interpretation
Enhanced features did not meaningfully improve ROC-AUC.

Estimated length: 3-4 pages

---

## 10. Feature Importance

### 10.1 Top Features

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | ability_minus_difficulty | 0.1761 |
| 2 | recent_accuracy_minus_difficulty | 0.1274 |
| 3 | question_difficulty_estimate | 0.1233 |
| 4 | question_accuracy_so_far | 0.1130 |
| 5 | elapsed_time_ratio_vs_question_avg | 0.0436 |

### 10.2 Educational Interpretation
Explain student ability vs question difficulty.

Estimated length: 3-4 pages

---

## 11. Error Analysis

### 11.1 Error by Student History

| Student History | Error Rate |
|---|---:|
| 0-4 attempts | 35.5% |
| 5-19 attempts | 33.9% |
| 20-49 attempts | 32.1% |
| 50-99 attempts | 32.4% |
| 100+ attempts | 30.9% |

### 11.2 Error by Question Difficulty

| Difficulty Group | Error Rate |
|---|---:|
| Easy | 22.4% |
| Medium | 36.6% |
| Hard | 37.4% |
| Very Hard | 28.9% |

### 11.3 Error by Model Confidence

| Confidence Group | Error Rate |
|---|---:|
| Low | 44.8% |
| Medium | 32.4% |
| High | 17.5% |
| Very High | 6.1% |

### 11.4 Interpretation
Explain what these errors mean for adaptive tutoring.

Estimated length: 5-6 pages

---

## 12. Discussion

### 12.1 What Worked Well
- Real-data validation
- Scale improvement
- Leakage-aware pipeline
- Explainable feature importance

### 12.2 What Did Not Improve
- Enhanced feature set did not outperform baseline
- Some probabilities were overconfident

### 12.3 Educational Meaning
Explain how this could support future tutor personalization.

Estimated length: 4-5 pages

---

## 13. Limitations

### 13.1 No New Algorithm
This is an applied ML research project, not a novel KT algorithm.

### 13.2 No Deep KT Baseline Yet
DKT, SAKT, and Transformer KT are future work.

### 13.3 Calibration Limitation
Some predicted probabilities appear overconfident.

### 13.4 Dataset Limitation
The project uses a subset of EdNet KT1.

Estimated length: 3-4 pages

---

## 14. Ethics and Responsible AI

### 14.1 Privacy
Raw educational data is kept local.

### 14.2 Bias and Fairness
Educational data may reflect unequal learning opportunities.

### 14.3 Human Oversight
AI tutor predictions should support, not replace, teachers.

### 14.4 Responsible Deployment
Predictions should not be used for high-stakes decisions without validation.

Estimated length: 3-4 pages

---

## 15. Future Work

### 15.1 Deep Knowledge Tracing
### 15.2 SAKT
### 15.3 Transformer-Based KT
### 15.4 Probability Calibration
### 15.5 Cold-Start Analysis
### 15.6 Stronger Recommendation System
### 15.7 More Realistic RL Tutor

Estimated length: 3-4 pages

---

## 16. Conclusion

Summarize:
- V1 synthetic prototype completed
- V2 EdNet validation completed
- Best real-data ROC-AUC: 0.7301
- Performance improved with scale
- Feature importance and error analysis support educational interpretation
- Project is strong applied ML research portfolio work

Estimated length: 2 pages

---

## References

Potential references to include later:
- EdNet paper
- Bayesian Knowledge Tracing
- Deep Knowledge Tracing
- SAKT
- Transformer-based KT
- Educational Data Mining papers
- scikit-learn documentation

Estimated length: 2-3 pages

---

## Appendix

### Appendix A: Repository Structure
### Appendix B: Config Files
### Appendix C: Feature List
### Appendix D: Full Model Metrics
### Appendix E: Reproducibility Commands
### Appendix F: Additional Result Tables

Estimated length: 6-8 pages

---

## Estimated Total Length

| Section Group | Estimated Pages |
|---|---:|
| Front Matter | 2-3 |
| Introduction + Background | 10-13 |
| Dataset + Methodology | 10-12 |
| Features + Models | 9-11 |
| Experiments + Results | 9-11 |
| Analysis + Discussion | 12-15 |
| Ethics + Future Work + Conclusion | 8-10 |
| References + Appendix | 8-11 |

Estimated final report length: 40-60 pages, depending on final manual writing depth.
