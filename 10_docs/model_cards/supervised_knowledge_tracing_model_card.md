# Supervised Knowledge Tracing Model Card

## 1. Model Purpose

This model card describes the supervised learning component of the Adaptive AI Tutor Research Lab.

The goal of this component is to predict whether a student is likely to answer a question correctly based on previous learning behavior, topic performance, question difficulty, and interaction history.

## 2. Task

The task is binary classification.

Target variable:

- `is_correct`

Possible values:

- `1`: the student answered correctly
- `0`: the student answered incorrectly

## 3. Input Features

The model uses engineered features such as:

- student accuracy so far
- previous answer correctness
- rolling accuracy
- topic-level accuracy
- question-level accuracy
- elapsed time
- question difficulty
- topic tag
- question history

These features are created before the current answer is used, helping reduce data leakage.

## 4. Models Tested

The project compares several supervised baseline models:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

The Dummy Classifier is used as a baseline to check whether real models perform better than a simple majority-class strategy.

## 5. Evaluation Metrics

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Log Loss

ROC-AUC is useful for checking how well the model separates correct and incorrect answers.

Log Loss is useful for evaluating the quality of predicted probabilities.

## 6. Intended Use

This model is intended for research and educational experimentation.

Possible uses:

- estimating student knowledge state
- identifying whether a student may struggle with a question
- supporting recommendation logic
- building an adaptive learning prototype

## 7. Not Intended Use

This model should not be used for high-stakes educational decisions.

It should not be used to:

- officially grade students
- replace teachers
- label students permanently
- decide academic opportunities
- make real classroom decisions without human review

## 8. Data

The current version uses synthetic student interaction data.

Synthetic data helps with:

- privacy protection
- reproducibility
- safe experimentation
- early prototype development

However, synthetic data does not fully represent real student behavior.

## 9. Limitations

Current limitations:

- the dataset is synthetic
- student behavior is simulated
- features are simplified
- real classroom feedback is not included
- long-term learning outcomes are not measured
- results may not transfer directly to real education settings

## 10. Ethical Considerations

Educational AI systems must be designed carefully because they can influence how students learn.

Important concerns include:

- privacy
- fairness
- transparency
- avoiding negative student labeling
- avoiding over-reliance on automated recommendations
- keeping humans involved in important educational decisions

## 11. Future Improvements

Future improvements may include:

- testing on real educational datasets
- adding deep knowledge tracing models
- adding fairness evaluation
- improving explainability
- comparing performance across different student groups
- testing long-term learning outcomes

## 12. Summary

The supervised knowledge tracing component provides a baseline for predicting student correctness.

It is an important part of the full adaptive tutor pipeline because it helps the system estimate student performance before making recommendations.