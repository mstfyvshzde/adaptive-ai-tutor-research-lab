---
title: "Adaptive AI Tutor Research Lab"
subtitle: "Real-Data Validation with EdNet KT1"
author: "Şahzadə Mustafayev"
date: "Version: v2.0-ednet"
---

# Adaptive AI Tutor Research Lab  
## Real-Data Validation with EdNet KT1

**Author:** Şahzadə Mustafayev  
**Repository:** `mstfyvshzde/adaptive-ai-tutor-research-lab`  
**Version:** `v2.0-ednet`  
**Project Type:** Applied Machine Learning Research Portfolio Project  
**Domain:** Educational Data Mining / Adaptive Learning / Knowledge Tracing  

---

# Abstract

Adaptive tutoring systems aim to personalize learning by modeling student behavior and selecting learning activities that match each learner's current state. This project investigates how student interaction data can be used to support an adaptive AI tutor pipeline. The work begins with a synthetic end-to-end prototype and then extends the system to real educational data using the EdNet KT1 dataset.

The main real-data task is student correctness prediction: predicting whether a student will answer a question correctly using prior interaction history and question-level signals. The project implements a leakage-aware feature engineering pipeline, supervised machine learning baselines, scale experiments, feature ablation, feature importance analysis, error analysis, and responsible AI documentation.

The V1 synthetic prototype achieved a high ROC-AUC of `0.9077`, but this result came from controlled simulated data. The V2 EdNet validation provides a more realistic benchmark. Across real-data subsets, performance improved as the number of interactions increased: ROC-AUC rose from `0.6250` at approximately 5k interactions to `0.7301` at approximately 500k interactions. The best real-data model was Gradient Boosting using the baseline history-based feature set.

The analysis shows that the strongest predictive signals are related to the relationship between student ability and question difficulty. Error analysis also shows that predictions become more reliable when more student history is available and when model confidence is higher. The project does not claim to introduce a new knowledge tracing algorithm. Instead, it demonstrates a reproducible applied machine learning validation pipeline for educational data mining and adaptive learning.

---

# Table of Contents

1. Introduction  
2. Background and Related Work  
3. Dataset  
4. Methodology  
5. Feature Engineering  
6. Models  
7. Experiments  
8. Results  
9. Ablation Study  
10. Feature Importance  
11. Error Analysis  
12. Discussion  
13. Limitations  
14. Ethics and Responsible AI  
15. Future Work  
16. Conclusion  
17. References  
18. Appendix  

---

# 1. Introduction

## 1.1 Project Motivation

Education is increasingly supported by digital learning platforms, online assessment systems, and AI-powered tutoring tools. These systems collect large amounts of interaction data, including student responses, question identifiers, timestamps, elapsed time, correctness, and topic metadata. The central challenge is not only collecting this data, but using it to make learning more personalized and effective.

An adaptive tutor should be able to answer questions such as:

- Is the student likely to answer the next question correctly?
- Is the current question too easy, too difficult, or appropriately challenging?
- Which students need extra support?
- Which concepts or question types are causing difficulty?
- How reliable is the model's prediction?
- Can the system recommend better learning activities?

This project was built to explore these questions through an end-to-end applied machine learning pipeline.

The project began with a synthetic prototype because synthetic data allows controlled testing without privacy risks. After the full pipeline was working, the project was extended to real educational data using EdNet KT1. This V2 extension is important because real educational data is noisier, larger, more diverse, and more difficult than synthetic data.

## 1.2 Problem Statement

The core real-data problem is binary correctness prediction.

Given a student's previous interactions and question-level information, the model predicts whether the student will answer the current question correctly.

The target variable is:

```text
is_correct = 1 if user_answer == correct_answer
is_correct = 0 otherwise
This is a supervised binary classification problem. The main evaluation metric is ROC-AUC, supported by accuracy, precision, recall, F1-score, and log loss.
1.3 Research Questions
This project is guided by the following research questions:
Can student correctness be predicted from previous interaction history?
Does real-data model performance improve as the dataset scale increases?
Which features are most predictive of correctness?
Does enhanced leakage-free feature engineering improve performance over the baseline feature set?
Where does the model make more errors?
How can the results support future adaptive tutoring decisions?
What limitations must be considered before using such predictions in real educational settings?
1.4 Project Contributions
The project contributes an applied research pipeline with the following components:
A synthetic adaptive tutor prototype.
Real-data validation on EdNet KT1.
Leakage-aware feature engineering.
Time-aware supervised correctness prediction.
Real-data scale experiments from approximately 5k to 500k interactions.
Baseline versus enhanced feature ablation.
Feature importance analysis.
Error analysis by confidence, history, and difficulty.
Responsible AI discussion.
Reproducible scripts and GitHub Actions CI.
Research-style report and visual outputs.
1.5 Scope
This project is not a novel knowledge tracing algorithm paper. It does not introduce a new neural architecture. Instead, it focuses on building a careful, reproducible, and interpretable applied machine learning pipeline.
The project is best understood as a strong applied machine learning research portfolio project in educational data mining.
2. Background and Related Work
2.1 Intelligent Tutoring Systems
Intelligent tutoring systems are designed to support learning by modeling student progress and adapting instruction. A traditional tutoring system may provide feedback, hints, or next questions based on a student's current performance. A modern AI tutor can extend this idea by using machine learning to estimate student knowledge, predict future performance, and recommend learning materials.
The key idea is personalization. A tutor should not treat all students in the same way. A student who is struggling may need easier or more targeted practice. A student who is performing well may need more challenging questions. A student with inconsistent performance may need review or diagnostic assessment.
2.2 Educational Data Mining
Educational data mining studies data generated by learning environments. This includes student answers, time spent, attempts, topic metadata, hints, video usage, and learning paths. The goal is to discover patterns that can improve teaching and learning.
In this project, the educational data mining task is focused on correctness prediction. Correctness prediction can support:
personalized question recommendation,
early detection of struggling students,
adaptive difficulty control,
student progress monitoring,
model-based learning analytics.
2.3 Knowledge Tracing
Knowledge tracing is the task of modeling how a student's knowledge changes over time. In many knowledge tracing tasks, the model observes a sequence of past student responses and predicts future performance.
A simplified knowledge tracing setup can be represented as:
past interactions → estimated student state → predicted future correctness
This project does not implement a full deep knowledge tracing model. However, it uses knowledge tracing-inspired features such as student accuracy so far, rolling accuracy, question difficulty estimates, and ability-minus-difficulty signals.
2.4 Bayesian Knowledge Tracing
Bayesian Knowledge Tracing is a classical approach to student modeling. It treats knowledge mastery as a hidden state and updates the probability of mastery after each student response.
BKT is important because it is interpretable. It connects student correctness to an estimated probability of mastery. However, it often depends on assumptions about skills, knowledge components, and manually structured domains.
This project does not implement BKT directly, but it follows the same broad motivation: using student response history to estimate future performance.
2.5 Deep Knowledge Tracing
Deep Knowledge Tracing introduced recurrent neural networks for modeling student response sequences. Instead of manually defining all knowledge states, DKT uses neural sequence modeling to learn patterns from interaction histories.
DKT is important because it showed that deep models can capture complex temporal patterns in student learning data. However, deep KT models may require more computation, careful tuning, and interpretability analysis.
This project leaves DKT as future work.
2.6 Attention-Based Knowledge Tracing
Attention-based knowledge tracing methods, such as SAKT and AKT, use attention mechanisms to identify which previous interactions are most relevant to the current prediction.
These models are useful for long student histories because not every previous interaction is equally important. Attention mechanisms can help the model focus on relevant previous questions, concepts, or responses.
This project does not yet implement SAKT or AKT. However, the EdNet KT1 sequence data makes these methods natural future baselines.
2.7 EdNet Dataset
EdNet is a large-scale hierarchical educational dataset collected from a real AI tutoring platform. It includes student interactions at multiple levels of abstraction and supports tasks such as knowledge tracing and learning path recommendation.
This project uses EdNet KT1, which focuses on question-solving interactions. KT1 is suitable for correctness prediction because it contains student question attempts and can be joined with question metadata to compute correctness.
2.8 Research Gap and Project Position
Many knowledge tracing papers focus on model architecture. This project takes a different applied direction. It focuses on:
building a clean repository,
validating a full ML pipeline,
avoiding data leakage,
testing scale effects,
comparing feature sets,
analyzing errors,
documenting ethics and limitations.
The contribution is therefore practical and engineering-oriented rather than algorithmically novel.
3. Dataset
3.1 Synthetic V1 Dataset
The project began with a synthetic dataset. Synthetic data was useful because it allowed the full adaptive tutor pipeline to be developed safely before introducing real data.
The synthetic prototype included:
student profiles,
question difficulty,
simulated correctness,
feature engineering,
supervised prediction,
clustering,
recommendations,
reinforcement learning tutor simulation,
dashboard visualization.
The synthetic result achieved ROC-AUC 0.9077. This high score should not be interpreted as real-world performance. Synthetic data is controlled and usually easier than real educational data.
3.2 EdNet KT1 Dataset
The V2 extension uses EdNet KT1. The local raw data includes:
KT1 student interaction files,
question metadata from contents/questions.csv,
question identifiers,
user answers,
elapsed time,
correct answers,
part metadata,
tags.
The main correctness label is computed as:
is_correct = user_answer == correct_answer
Raw EdNet files are intentionally kept local and excluded from GitHub.
3.3 Data Scope
The final real-data subset contains:
Dataset	Interactions	Students	Questions
EdNet 500k Final	500,057	6,419	11,424
The project also runs smaller scale experiments:
Stage	Interactions
EdNet 5k	5,017
EdNet 50k	50,081
EdNet 200k	200,091
EdNet 500k Final	500,057
3.4 Raw Data Policy
Raw educational data is not committed to GitHub. This is important for:
repository size,
reproducibility boundaries,
privacy-aware practice,
licensing and responsible data handling.
The repository commits code, reports, result tables, and selected figures, but not large raw dataset files.
3.5 Data Preparation
The V2 workflow includes:
Inspect EdNet files.
Validate schema.
Join student interactions with question metadata.
Compute correctness.
Construct subsets at multiple scales.
Build leakage-aware features.
Train supervised models.
Evaluate and report results.
4. Methodology
4.1 Overall Pipeline
The overall V2 pipeline is:
EdNet raw data
→ schema validation
→ subset construction
→ correctness labeling
→ leakage-aware feature engineering
→ supervised model training
→ evaluation
→ ablation analysis
→ feature importance
→ error analysis
→ reporting
This pipeline is designed to be realistic and reproducible. It separates data preparation, features, models, evaluation, and reporting into different scripts.
4.2 Leakage-Aware Design
Data leakage happens when information from the target or future observations is accidentally used as input. In correctness prediction, this would create unrealistically high results.
For example, if the current row's correctness is used to compute the current row's student accuracy feature, the model would indirectly see the answer it is supposed to predict.
To prevent this, history-based features are computed using previous interactions only. This includes:
cumulative counts excluding current row,
cumulative accuracy excluding current row,
rolling accuracy shifted by one interaction,
question accuracy based on previous attempts,
difficulty estimates based on previous attempts.
4.3 Time-Based Split
Educational prediction is naturally temporal. A model should use past interactions to predict future performance.
A random split can mix future observations into training, producing overly optimistic results. A time-based split better simulates deployment because the model is evaluated on later interactions.
4.4 Evaluation Metrics
The project uses multiple metrics:
Metric	Purpose
ROC-AUC	Main ranking quality metric
Accuracy	Overall correct classification rate
Precision	Correctness of positive predictions
Recall	Ability to find correct responses
F1-score	Balance between precision and recall
Log Loss	Quality of predicted probabilities
ROC-AUC is the main metric because it measures the model's ability to rank correct responses above incorrect responses across thresholds.
4.5 Reproducibility
The repository supports reproducibility through:
structured scripts,
committed result tables,
committed visual outputs,
GitHub Actions CI,
documented run commands,
clear local raw data policy.
5. Feature Engineering
5.1 Baseline Features
The baseline feature set includes history-based student and question signals.
Examples include:
student attempt count so far,
student correct count so far,
student accuracy so far,
question attempt count so far,
question accuracy so far,
question difficulty estimate,
elapsed time,
part metadata,
tag metadata.
These features are simple but meaningful. They represent the idea that correctness depends on both the student and the question.
5.2 Enhanced Features
The enhanced feature set adds more detailed learning signals:
rolling accuracy over recent interactions,
student correct streak,
student incorrect streak,
student average elapsed time so far,
student elapsed time variability,
question average elapsed time so far,
same-question seen-before flag,
activity gap in hours,
tag count,
ability-minus-difficulty signal,
recent-accuracy-minus-difficulty signal,
elapsed-time ratio versus student average,
elapsed-time ratio versus question average.
5.3 Leakage Prevention in Features
The enhanced feature builder avoids using current correctness as input. For example:
student_accuracy_so_far = previous_correct_answers / previous_attempts
not:
student_accuracy_including_current = all_correct_answers_including_current / all_attempts_including_current
This distinction is essential.
5.4 Educational Interpretation
The most important feature concept is the match between student ability and question difficulty.
If a student's recent accuracy is high and the question difficulty is low, the model should predict a higher probability of correctness. If a student's recent accuracy is low and the question is difficult, the model should predict lower correctness.
This is educationally meaningful because adaptive tutoring depends on matching students with appropriate challenge levels.
6. Models
6.1 Dummy Majority Baseline
The dummy model predicts the majority class. It is not expected to perform well, but it provides a minimum baseline. Any useful model should outperform the dummy baseline.
6.2 Logistic Regression
Logistic Regression is a simple and interpretable linear model. It is useful as a baseline because it shows how much predictive power can be captured with linear relationships.
Strengths:
simple,
fast,
interpretable,
good baseline.
Limitations:
limited nonlinear modeling,
may underfit complex educational patterns.
6.3 Random Forest
Random Forest is an ensemble of decision trees. It can model nonlinear relationships and interactions between features.
Strengths:
handles nonlinear patterns,
robust to many feature types,
useful for feature importance.
Limitations:
less interpretable than logistic regression,
can be slower,
probability calibration may be imperfect.
6.4 Gradient Boosting
Gradient Boosting builds trees sequentially, where each tree tries to correct previous errors. It performed best in the main EdNet scale experiments.
Strengths:
strong tabular-data performance,
handles nonlinear interactions,
effective with engineered features.
Limitations:
can overfit if not tuned carefully,
less transparent than simple models.
6.5 Histogram Gradient Boosting
Histogram Gradient Boosting is an efficient gradient boosting variant. It can be useful for larger tabular datasets.
Strengths:
efficient,
strong for structured data,
handles larger datasets well.
Limitations:
still requires careful evaluation,
may not always outperform standard Gradient Boosting.
7. Experiments
7.1 V1 Synthetic Experiment
The V1 synthetic experiment tested the full adaptive tutor pipeline on controlled data.
Result:
Stage	Data Source	Interactions	Best Model	ROC-AUC
V1 Synthetic	Synthetic prototype data	1,452	Logistic Regression	0.9077
This result shows that the pipeline works technically. However, it is not directly comparable to real-data performance.
7.2 EdNet Scale Experiments
The V2 scale experiments test whether performance improves as more real student interaction data is used.
The stages are:
EdNet 5k pilot,
EdNet 50k small,
EdNet 200k medium,
EdNet 500k final.
7.3 Experimental Setup
Each experiment uses the same broad prediction task:
Input: previous student/question interaction signals
Output: probability of correctness
The main difference between experiments is dataset scale.
7.4 Expected Behavior
The expected behavior is that performance should improve with more data because the model has more student histories, more question attempts, and more examples of correctness patterns.
8. Results
8.1 Main Result Table
Stage	Data Source	Interactions	Best Model	ROC-AUC
V1 Synthetic	Synthetic prototype data	1,452	Logistic Regression	0.9077
EdNet 5k	Real EdNet KT1	5,017	Gradient Boosting	0.6250
EdNet 50k	Real EdNet KT1	50,081	Gradient Boosting	0.7080
EdNet 200k	Real EdNet KT1	200,091	Gradient Boosting	0.7222
EdNet 500k Final	Real EdNet KT1	500,057	Gradient Boosting	0.7301
8.2 Scale Trend
The EdNet real-data results show a clear scale trend:
5k interactions   → ROC-AUC 0.6250
50k interactions  → ROC-AUC 0.7080
200k interactions → ROC-AUC 0.7222
500k interactions → ROC-AUC 0.7301
The largest improvement occurs between 5k and 50k interactions. After that, performance continues to improve, but the improvement becomes smaller.
8.3 Interpretation
The scale trend suggests that the model benefits from more student interaction history. This is expected because many features depend on historical behavior. With more data, the model can better estimate:
student accuracy so far,
question difficulty,
question accuracy,
student-question match,
stable behavioral patterns.
8.4 Synthetic vs Real Data
The synthetic ROC-AUC is much higher than the EdNet ROC-AUC. This is expected.
Synthetic data is controlled by the rules used to generate it. Real data includes noise, missing context, diverse student behavior, inconsistent effort, question differences, and many uncontrolled factors.
Therefore, the EdNet 500k result is more meaningful for real-world evaluation.
9. Ablation Study
9.1 Motivation
The enhanced feature set was created to test whether richer leakage-free features improve prediction performance.
The expectation was that rolling accuracy, streaks, activity gaps, elapsed-time ratios, and ability-minus-difficulty signals might improve ROC-AUC.
9.2 Results
Feature Set	Best Model	Accuracy	F1	ROC-AUC	Log Loss
Baseline Features	Gradient Boosting	0.6799	0.7523	0.7301	0.5939
Enhanced Features	Random Forest	0.6771	0.7557	0.7298	0.5956
9.3 Interpretation
The enhanced feature set achieved comparable performance but did not meaningfully improve ROC-AUC.
This is an important result. It shows that not every additional feature improves model performance. It also suggests that the baseline history-based features already captured much of the available predictive signal.
The enhanced feature set still provides useful interpretation, especially through feature importance and error analysis.
10. Feature Importance
10.1 Top Features
Rank	Feature	Importance
1	ability_minus_difficulty	0.1761
2	recent_accuracy_minus_difficulty	0.1274
3	question_difficulty_estimate	0.1233
4	question_accuracy_so_far	0.1130
5	elapsed_time_ratio_vs_question_avg	0.0436
10.2 Educational Interpretation
The most important features are not random technical variables. They have direct educational meaning.
The top features suggest that correctness depends heavily on:
student ability,
recent performance,
estimated question difficulty,
historical question success rate,
time spent relative to question norms.
This supports the idea that an adaptive tutor should not only ask whether a student is generally strong or weak. It should ask whether the current question is appropriate for the student's current level.
10.3 Ability-Minus-Difficulty
The feature ability_minus_difficulty captures the relationship between estimated student ability and estimated question difficulty.
A positive value suggests the student may be stronger than the question difficulty. A negative value suggests the question may be too difficult relative to the student's history.
This is useful for adaptive learning because it can guide difficulty selection.
11. Error Analysis
11.1 Error by Student History
Student History	Error Rate
0-4 attempts	35.5%
5-19 attempts	33.9%
20-49 attempts	32.1%
50-99 attempts	32.4%
100+ attempts	30.9%
The model becomes more reliable when more student history is available. This is expected because history-based features are weak when a student has very few previous interactions.
11.2 Error by Question Difficulty
Difficulty Group	Error Rate
Easy	22.4%
Medium	36.6%
Hard	37.4%
Very Hard	28.9%
The model makes more errors on medium and hard questions. This may happen because these questions are less predictable: some students answer them correctly and others incorrectly depending on subtle ability differences.
The lower error for very hard questions may occur because many students are predicted to struggle, making the class pattern more consistent.
11.3 Error by Model Confidence
Confidence Group	Error Rate
Low	44.8%
Medium	32.4%
High	17.5%
Very High	6.1%
Model confidence is strongly related to prediction accuracy. When confidence is very high, error rate is much lower. When confidence is low, error rate is much higher.
This matters for adaptive tutoring. A tutor could use confidence to decide whether to trust the prediction or request more evidence.
11.4 Practical Meaning
Error analysis suggests that an adaptive tutor should be careful in cold-start situations. When student history is limited, predictions are less reliable.
A responsible tutor should not overreact to early predictions. It should collect more evidence and avoid making strong conclusions from very few interactions.
12. Discussion
12.1 What Worked Well
Several parts of the project worked well.
First, the transition from synthetic data to real EdNet data was successful. The project moved beyond a toy prototype and validated the pipeline on real educational interactions.
Second, the leakage-aware feature engineering approach was important. It kept the evaluation more realistic and prevented artificially inflated performance.
Third, scale experiments produced a meaningful trend. Performance improved as the number of interactions increased.
Fourth, feature importance and error analysis created interpretable educational insights.
12.2 What Did Not Improve
The enhanced feature set did not meaningfully outperform the baseline feature set. This is not a failure. It is a useful research result.
It shows that more features are not automatically better. It also suggests that the baseline features already contained strong signals.
12.3 Model Reliability
The model is not equally reliable in all cases. It performs better when:
more student history exists,
model confidence is high,
question difficulty is easier or more predictable.
It performs worse when:
student history is limited,
model confidence is low,
question difficulty is ambiguous.
12.4 Educational Meaning
The project supports a practical idea: adaptive learning systems should consider both student ability and question difficulty.
A future tutor could use these predictions to:
recommend easier questions when the student is struggling,
recommend harder questions when the student is performing well,
identify uncertain cases,
avoid high-stakes decisions when confidence is low.
13. Limitations
13.1 No New Algorithm
This project does not introduce a new knowledge tracing model or neural architecture. It is an applied validation pipeline.
13.2 No Deep KT Baselines Yet
The project does not yet compare against:
Deep Knowledge Tracing,
SAKT,
AKT,
Transformer-based knowledge tracing models.
These are important future baselines.
13.3 Probability Calibration
Some predicted probabilities appear overconfident. For example, in one analysis group, predicted correctness was much higher than actual correctness.
Future work should include calibration methods such as:
Platt scaling,
isotonic regression,
calibration curves,
expected calibration error.
13.4 Dataset Subset Limitation
The project uses a subset of EdNet KT1 rather than the entire dataset. This is reasonable for a portfolio-scale research project, but future work could test larger subsets.
13.5 Learning Outcome Limitation
The current task predicts correctness. It does not directly measure long-term learning, retention, motivation, or conceptual understanding.
13.6 Deployment Limitation
The model is not ready for high-stakes educational decisions. It should be treated as a decision-support tool only.
14. Ethics and Responsible AI
14.1 Privacy
Educational data can be sensitive. Student behavior, performance, and learning history should be handled carefully.
This project keeps raw EdNet data local and does not commit raw data to GitHub.
14.2 Bias and Fairness
Educational data may reflect unequal access to preparation, technology, time, and support. A model trained on such data may learn patterns that reflect these inequalities.
Future work should include fairness analysis across meaningful groups when such metadata is available and ethically appropriate.
14.3 Human Oversight
AI tutor predictions should support human decision-making, not replace teachers or educational experts.
A prediction such as "student likely incorrect" should not be treated as a final judgment about the student. It should be treated as a signal that may help provide support.
14.4 Responsible Deployment
Responsible deployment requires:
monitoring model performance,
checking calibration,
avoiding high-stakes automation,
explaining predictions,
allowing human review,
protecting student data.
14.5 Transparency
The project reports limitations clearly. It does not claim to solve adaptive tutoring fully. It presents results, weaknesses, and future work honestly.
15. Future Work
15.1 Deep Knowledge Tracing
Implement DKT using student response sequences and compare it against the current classic ML baselines.
15.2 SAKT and AKT
Add attention-based knowledge tracing models to evaluate whether attention improves predictive performance on EdNet KT1.
15.3 Transformer-Based Knowledge Tracing
Experiment with Transformer-based student sequence modeling.
15.4 Calibration
Apply probability calibration and evaluate whether predicted probabilities better match actual correctness.
15.5 Cold-Start Analysis
Study model performance for:
new students,
new questions,
low-history students,
rare tags.
15.6 Recommendation System
Connect correctness prediction to a stronger recommendation system that selects the next question based on student state and predicted challenge level.
15.7 Reinforcement Learning Extension
Move the reinforcement learning tutor from synthetic simulation toward a more realistic offline evaluation setting.
15.8 Fairness and Robustness
Add fairness and robustness analysis to evaluate whether the model behaves consistently across student groups or question categories.
15.9 Dashboard Improvement
Improve the Streamlit demo to include:
EdNet visual results,
confidence analysis,
student history analysis,
feature importance,
model explanation.
16. Conclusion
This project successfully extends a synthetic adaptive AI tutor prototype into a real-data educational machine learning validation pipeline using EdNet KT1.
The key result is that real-data performance improves with scale. ROC-AUC increased from 0.6250 at approximately 5k interactions to 0.7301 at approximately 500k interactions. The best real-data model was Gradient Boosting with the baseline feature set.
The project also shows that the strongest predictive signals are educationally meaningful. Features related to student ability, recent performance, and question difficulty were the most important. Error analysis showed that predictions become more reliable when more student history is available and when model confidence is higher.
The project is not a new knowledge tracing algorithm paper. Its value is in building a clean, reproducible, leakage-aware applied ML research pipeline with real-data validation, honest limitations, visual reporting, CI, and responsible AI discussion.
Overall, the project demonstrates strong applied machine learning research practice in educational data mining and provides a foundation for future work in deep knowledge tracing, attention-based models, calibration, recommendation, and adaptive tutoring.
17. References
Abdelrahman, G., Wang, Q., & Nunes, B. P. (2022). Knowledge Tracing: A Survey. arXiv:2201.06953.
Choi, Y., Lee, Y., Shin, D., Cho, J., Park, S., Lee, S., Baek, J., Bae, C., Kim, B., & Heo, J. (2019). EdNet: A Large-Scale Hierarchical Dataset in Education. arXiv:1912.03072.
Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. User Modeling and User-Adapted Interaction.
Ghosh, A., Heffernan, N., & Lan, A. S. (2020). Context-Aware Attentive Knowledge Tracing. arXiv:2007.12324.
Khajah, M., Lindsey, R. V., & Mozer, M. C. (2016). How Deep Is Knowledge Tracing? arXiv:1604.02416.
Pandey, S., & Karypis, G. (2019). A Self-Attentive Model for Knowledge Tracing. arXiv:1907.06837.
Piech, C., Spencer, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. (2015). Deep Knowledge Tracing. arXiv:1506.05908.
Shen, S., Liu, Q., Huang, Z., Zheng, Y., Yin, M., Wang, M., & Chen, E. (2021). A Survey of Knowledge Tracing: Models, Variants, and Applications. arXiv:2105.15106.
18. Appendix
Appendix A: Repository Structure
adaptive-ai-tutor-research-lab/
├── 00_project_charter/
├── 01_research/
├── 02_data/
├── 03_notebooks/
├── 04_src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── rl/
│   ├── evaluation/
│   └── visualization/
├── 05_experiments/
├── 06_results/
│   ├── reports/
│   ├── tables/
│   └── figures/
├── 07_demo/
├── 08_report/
├── 09_portfolio_assets/
├── 10_docs/
├── tests/
├── run_pipeline.py
├── requirements.txt
└── README.md
Appendix B: Main V2 Scripts
04_src/data/inspect_ednet_files.py
04_src/data/ednet_schema.py
04_src/data/prepare_ednet_subset.py
04_src/data/validate_ednet_dataset.py
04_src/features/build_ednet_features.py
04_src/features/build_ednet_features_v2.py
04_src/models/ednet_supervised_baselines.py
04_src/models/ednet_enhanced_models.py
04_src/evaluation/compare_ednet_feature_sets.py
04_src/evaluation/build_final_v1_v2_comparison.py
04_src/evaluation/analyze_ednet_feature_importance.py
04_src/evaluation/analyze_ednet_errors.py
04_src/visualization/create_ednet_final_figures.py
Appendix C: Important Output Files
06_results/tables/ednet/final_v1_v2_comparison.csv
06_results/tables/ednet/ednet_feature_ablation_500k.csv
06_results/tables/ednet/ednet_feature_importance.csv
06_results/tables/ednet/ednet_error_analysis.csv
06_results/reports/final_ednet_v2_report.md
06_results/reports/final_ednet_v2_paper.md
06_results/reports/final_report_outline_harvard_style.md
10_docs/related_work_references.md
Appendix D: Figure Outputs
06_results/figures/ednet/pipeline_diagram.png
06_results/figures/ednet/roc_auc_by_scale.png
06_results/figures/ednet/feature_ablation.png
06_results/figures/ednet/top_feature_importance.png
06_results/figures/ednet/error_by_confidence.png
06_results/figures/ednet/error_by_student_history.png
06_results/figures/ednet/error_by_difficulty.png
Appendix E: Reproducibility Commands
Create environment:
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Run tests:
python -m compileall 04_src run_pipeline.py tests
python -m pytest -q
Run EdNet V2 workflow:
python 04_src/data/validate_ednet_dataset.py
python 04_src/features/build_ednet_features.py
python 04_src/models/ednet_supervised_baselines.py
python 04_src/features/build_ednet_features_v2.py
python 04_src/models/ednet_enhanced_models.py
python 04_src/evaluation/compare_ednet_feature_sets.py
python 04_src/evaluation/analyze_ednet_feature_importance.py
python 04_src/evaluation/analyze_ednet_errors.py
python 04_src/evaluation/build_final_v1_v2_comparison.py
python 04_src/visualization/create_ednet_final_figures.py
Appendix F: Final Result Summary
Stage	Interactions	Best Model	ROC-AUC
V1 Synthetic	1,452	Logistic Regression	0.9077
EdNet 5k	5,017	Gradient Boosting	0.6250
EdNet 50k	50,081	Gradient Boosting	0.7080
EdNet 200k	200,091	Gradient Boosting	0.7222
EdNet 500k Final	500,057	Gradient Boosting	0.7301
Appendix G: Final Assessment
This project demonstrates:
applied ML research design,
real educational dataset validation,
leakage-aware feature engineering,
supervised learning evaluation,
scale testing,
ablation study,
model interpretation,
error analysis,
responsible AI discussion,
GitHub CI,
visual reporting,
reproducible project structure.
It is a strong applied machine learning portfolio project and a solid foundation for deeper future work in knowledge tracing and adaptive tutoring.
EOF

## 2) Kontrol et

```bash id="4fisxf"
wc -l 06_results/reports/final_ednet_v2_paper.md
grep -n "Figure\|figures/ednet\|References\|Conclusion" 06_results/reports/final_ednet_v2_paper.md
3) Commit + push
git add 06_results/reports/final_ednet_v2_paper.md
git commit -m "Add final EdNet V2 paper source"
git push origin main