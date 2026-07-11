# Presentation Outline

## 1. Opening

Project name:

Adaptive AI Tutor Research Lab

One-sentence explanation:

This project explores how an AI tutor can personalize learning using student interaction history, supervised learning, recommendation strategies, and reinforcement learning.

## 2. Problem

Many online learning systems give similar content to different students.

However, students have different strengths, weaknesses, speeds, and learning histories.

The project asks:

Can an AI tutor use student data to make more personalized learning decisions?

## 3. Data

The current version uses synthetic student interaction data.

Each row represents a student answering a question.

The dataset includes:

- student ID
- question ID
- topic
- difficulty
- elapsed time
- correctness

Synthetic data was used for privacy, reproducibility, and safe prototyping.

## 4. Pipeline

The full pipeline is:

data generation → validation → feature engineering → supervised prediction → clustering → recommendation → reinforcement learning → evaluation → visualization → demo

The full project can be run with:

`python run_pipeline.py`

Tests can be run with:

`pytest`

## 5. Supervised Learning

The supervised learning component predicts whether a student will answer correctly.

Models used:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

Metrics used:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- Log Loss

## 6. Student Clustering

The clustering component groups students based on learning behavior.

It looks at features such as:

- total attempts
- final accuracy
- recent accuracy
- topic diversity
- average difficulty
- progress trend

## 7. Recommendation System

The recommendation component creates simple tutor strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

This answers:

What should the student practice next?

## 8. Reinforcement Learning

The RL component simulates an adaptive tutor.

The tutor observes a state, chooses an action, receives reward, and learns over time.

State:

- recent accuracy
- weak topic
- current step

Actions:

- easy
- medium
- hard

The Q-learning tutor is compared with a random policy.

## 9. Demo

The Streamlit demo shows:

- dataset overview
- supervised model results
- clustering results
- recommendation examples
- reinforcement learning comparison

Demo command:

`streamlit run 07_demo/app.py`

## 10. Main Strengths

The project is strong because it includes:

- complete ML pipeline
- multiple AI/ML methods
- automated testing
- visualization
- Streamlit demo
- documentation
- model cards
- ethics discussion
- real dataset upgrade plan

## 11. Limitations

The current version uses synthetic data.

The RL environment is simplified.

The recommendation strategies are baseline methods.

The system is a research prototype, not a production educational platform.

## 12. Future Work

Next improvements:

- use real educational datasets
- add deep knowledge tracing
- improve recommendation logic
- make RL environment more realistic
- add fairness evaluation
- improve interactive demo

## 13. Closing

This project helped me connect different AI/ML ideas into one complete adaptive learning system.

It shows not only model training, but also project structure, evaluation, testing, documentation, and demo presentation.