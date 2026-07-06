# Adaptive AI Tutor Research Lab — Project Report

## 1. Abstract

This project explores an adaptive AI tutoring system that combines knowledge tracing, student behavior clustering, recommender systems, and reinforcement learning.

The main goal is to simulate how an AI tutor can estimate a student's learning state and recommend better next learning activities over time.

This first version uses a synthetic demo dataset to build and test the full research pipeline.

## 2. Problem Statement

Many learning platforms provide the same content to all students.

However, students differ in:

- current knowledge level
- topic weaknesses
- learning speed
- consistency
- response accuracy

An adaptive tutor should use student interaction data to personalize the next learning activity.

## 3. Research Question

Can an adaptive AI tutor improve learning recommendations by combining student knowledge features, recommender systems, and reinforcement learning?

## 4. Dataset

This version uses a synthetic demo dataset.

The dataset includes:

- student IDs
- question IDs
- question topics
- question difficulty
- elapsed time
- correctness labels
- timestamps

The synthetic dataset is used only to test the architecture and pipeline.

Future versions should use real educational datasets such as EdNet or ASSISTments.

## 5. Methodology

### 5.1 Feature Engineering

The project creates features such as:

- student accuracy so far
- rolling accuracy
- previous correctness
- topic accuracy
- question difficulty estimate
- time since previous attempt

These features help model the student's learning state.

### 5.2 Supervised Knowledge Tracing

Supervised models are trained to predict whether a student will answer a question correctly.

Baseline models include:

- dummy classifier
- logistic regression
- random forest
- gradient boosting

The goal is to compare simple and stronger supervised baselines.

### 5.3 Student Behavior Clustering

Students are grouped based on learning behavior features such as:

- total attempts
- final accuracy
- average elapsed time
- topic diversity
- recent accuracy
- accuracy change

This helps identify different learner profiles.

### 5.4 Recommendation Baselines

The project tests simple recommendation strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

These baselines provide a starting point for adaptive learning recommendations.

### 5.5 Reinforcement Learning

A simple RL tutor environment is created.

In this environment:

- state represents student learning condition
- action represents choosing easy, medium, or hard questions
- reward represents whether the decision was useful

A random policy is compared with a Q-learning agent.

## 6. Evaluation

The project evaluates:

- supervised model performance
- student cluster summaries
- recommendation examples
- RL policy comparison
- reward curves

Main metrics include:

- accuracy
- precision
- recall
- F1-score
- ROC-AUC
- log loss
- average reward
- average correctness

## 7. Current Results

The first complete demo pipeline runs successfully.

It generates:

- demo dataset
- engineered features
- supervised baseline results
- student clusters
- recommendation examples
- RL policy results
- visualizations
- Streamlit demo

Detailed numerical results will be updated after final experiments.

## 8. Limitations

This project currently uses synthetic data.

Therefore, the results should not be interpreted as real-world educational impact.

The RL environment is also simplified and does not represent the full complexity of human learning.

## 9. Future Work

Future improvements include:

- using real datasets such as EdNet or ASSISTments
- adding stronger knowledge tracing models
- improving recommendation evaluation
- testing deeper RL methods
- building a better student simulator
- creating a more polished demo interface
- writing a full academic-style PDF report

## 10. Conclusion

This project demonstrates a complete research-style AI tutoring pipeline.

It connects supervised learning, clustering, recommender systems, and reinforcement learning into one adaptive learning system.

The current version is a strong first foundation for a more advanced AI education research project.
