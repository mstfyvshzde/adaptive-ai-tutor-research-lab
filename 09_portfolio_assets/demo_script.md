# Demo Script

## Project Name

Adaptive AI Tutor Research Lab

## Short Introduction

Hi, this is my Adaptive AI Tutor Research Lab project.

The goal of this project is to explore how an AI tutor can personalize learning using student interaction data.

The system combines supervised learning, student clustering, recommendation strategies, reinforcement learning, evaluation, visualization, and a Streamlit demo.

## Problem

In online learning platforms, students often receive the same learning path even though they have different strengths, weaknesses, and learning histories.

This project asks:

Can an AI tutor use student history to make more personalized learning decisions?

## Dataset

The current version uses synthetic student interaction data.

Each row represents a student answering a question.

The dataset includes:

- student ID
- question ID
- topic
- difficulty
- elapsed time
- correctness

Synthetic data is used because this is an early research prototype and avoids privacy risks.

## Pipeline

The full pipeline includes:

1. Data generation
2. Data validation
3. Feature engineering
4. Supervised knowledge tracing
5. Student clustering
6. Recommendation examples
7. Reinforcement learning tutor simulation
8. Evaluation
9. Visualization
10. Streamlit demo

Main command:

`python run_pipeline.py`

Test command:

`pytest`

## Supervised Learning

The supervised learning part predicts whether a student will answer a question correctly.

It uses features such as:

- previous accuracy
- rolling accuracy
- topic-level performance
- question difficulty
- elapsed time

Models include:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

The goal is to compare real models against a simple baseline.

## Clustering

The clustering part groups students based on learning behavior.

It uses features such as:

- total attempts
- final accuracy
- recent accuracy
- average elapsed time
- topic diversity
- accuracy change

This helps identify different student learning patterns.

## Recommendation System

The recommendation system creates simple tutor recommendations.

It includes:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

The goal is to answer:

What should the student practice next?

## Reinforcement Learning

The reinforcement learning part simulates an adaptive tutor.

The tutor observes a student state, chooses easy, medium, or hard questions, and receives reward based on student performance.

A Q-learning tutor is compared against a random policy.

The goal is to test whether the tutor can learn better decisions over time.

## Streamlit Demo

The Streamlit demo shows:

- dataset overview
- supervised model results
- clustering results
- recommendation examples
- reinforcement learning comparison

Demo command:

`streamlit run 07_demo/app.py`

## Main Strength

The strength of this project is that it is not just a single notebook.

It is a complete research-style AI/ML system with:

- clean project structure
- reproducible pipeline
- automated test
- multiple ML components
- visual results
- demo app
- documentation
- model cards
- ethics discussion

## Limitations

The current project uses synthetic data and simplified tutoring logic.

It is not a production-ready education system.

It is a research prototype that can later be improved with real datasets such as ASSISTments or EdNet.

## Future Work

Future improvements include:

- real educational datasets
- deep knowledge tracing
- stronger recommender systems
- more realistic reinforcement learning
- fairness evaluation
- explainable AI methods
- improved interactive demo

## Final Closing

This project helped me connect multiple AI/ML concepts into one complete adaptive learning system.

It demonstrates my ability to build an end-to-end machine learning project with data, modeling, evaluation, documentation, testing, and demo presentation.
