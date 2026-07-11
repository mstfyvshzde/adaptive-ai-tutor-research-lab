# Glossary

## Adaptive AI Tutor

A system that adjusts learning recommendations based on student behavior, performance, and learning history.

In this project, the tutor predicts student performance, recommends practice activities, and simulates adaptive decisions.

## Knowledge Tracing

Knowledge tracing is the task of estimating a student's knowledge state over time.

In this project, supervised learning models predict whether a student is likely to answer a question correctly.

## Student Interaction

A record of a student answering a question.

It may include student ID, question ID, topic, difficulty, elapsed time, and correctness.

## Feature Engineering

The process of converting raw data into useful machine learning inputs.

Examples in this project include student accuracy so far, rolling accuracy, topic-level accuracy, and question difficulty estimate.

## Data Leakage

Data leakage happens when a model accidentally uses future information that would not be available at prediction time.

This project tries to reduce leakage by using historical features before the current answer.

## Baseline Model

A simple model used for comparison.

In this project, the Dummy Classifier is a baseline for supervised learning, and random policy is a baseline for reinforcement learning.

## Dummy Classifier

A very simple model that predicts the majority class.

It helps check whether real machine learning models are actually better than a basic strategy.

## Logistic Regression

A supervised learning model used for classification.

In this project, it predicts whether a student will answer correctly.

## Random Forest

A machine learning model that uses many decision trees.

It is useful for capturing non-linear patterns in data.

## Gradient Boosting

A machine learning method that builds models step by step, with each new model trying to fix previous errors.

## Accuracy

The percentage of predictions that are correct.

Accuracy is useful, but it may not be enough when classes are imbalanced.

## Precision

Precision measures how many predicted positive cases were actually positive.

In this project, it helps evaluate correct-answer predictions.

## Recall

Recall measures how many actual positive cases were found by the model.

## F1 Score

F1 Score combines precision and recall into one metric.

It is useful when both false positives and false negatives matter.

## ROC-AUC

ROC-AUC measures how well a model separates two classes.

In this project, it measures how well the model separates correct and incorrect answers.

## Log Loss

Log Loss measures the quality of probability predictions.

Lower Log Loss usually means better probability estimates.

## Clustering

Clustering groups similar data points together.

In this project, students are grouped based on learning behavior.

## K-Means

A clustering algorithm that groups data into K clusters.

In this project, it is used to find student behavior groups.

## Silhouette Score

A metric that measures how well-separated clusters are.

Higher values usually mean better cluster separation.

## Recommendation System

A system that suggests items or activities.

In this project, the recommender suggests questions or practice activities for students.

## Random Recommendation

A recommendation strategy that selects a question randomly.

It is used as a simple baseline.

## Difficulty-Based Recommendation

A strategy that recommends easy, medium, or hard questions based on recent student accuracy.

## Weak-Topic Recommendation

A strategy that recommends questions from the topic where the student has the lowest performance.

## Reinforcement Learning

A machine learning approach where an agent learns by taking actions and receiving rewards.

In this project, the tutor learns which question difficulty to choose.

## Agent

The decision-maker in reinforcement learning.

In this project, the AI tutor is the agent.

## Environment

The world where the agent acts.

In this project, the tutoring simulation is the environment.

## State

The current situation observed by the agent.

In this project, state includes recent accuracy, weak topic, and session step.

## Action

A decision made by the agent.

In this project, actions are easy, medium, or hard question choices.

## Reward

The feedback received after an action.

In this project, reward increases when the student answers correctly or practices a weak topic.

## Q-Learning

A reinforcement learning algorithm that learns values for state-action pairs.

In this project, Q-learning helps the tutor learn better difficulty choices over time.

## Streamlit

A Python tool for building simple interactive data apps.

In this project, Streamlit is used to create the demo dashboard.

## Reproducibility

The ability to run the project again and get similar results.

This project supports reproducibility with a full pipeline command and automated test.

## Smoke Test

A basic test that checks whether the main system runs successfully.

In this project, the smoke test runs the full pipeline and checks that expected outputs are created.