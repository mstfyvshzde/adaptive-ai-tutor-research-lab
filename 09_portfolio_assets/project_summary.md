# Adaptive AI Tutor Research Lab — Portfolio Summary

## Project Title

Adaptive AI Tutor: Personalized Learning with Knowledge Tracing, Recommendation Systems, and Reinforcement Learning

## One-Sentence Summary

This project builds a research-style AI tutor pipeline that models student learning behavior, predicts answer correctness, recommends personalized learning activities, and simulates adaptive tutoring decisions using reinforcement learning.

## Project Type

AI/ML Research Portfolio Project

## Main Goal

The goal of this project is to explore how an AI tutor can use student interaction history to make more personalized learning decisions.

Instead of only predicting student performance, the project connects multiple AI components into one complete tutoring pipeline:

data → features → prediction → clustering → recommendation → reinforcement learning → evaluation → demo

## Key Components

### 1. Synthetic Student Learning Data

The project creates a synthetic student interaction dataset with students, questions, topics, difficulty levels, response times, and correctness labels.

This makes the project reproducible and avoids privacy risks during early development.

### 2. Feature Engineering

The project transforms raw interactions into machine learning features such as:

- student accuracy so far
- previous correctness
- rolling accuracy
- topic-level performance
- question-level performance
- elapsed time
- question difficulty

### 3. Supervised Knowledge Tracing

The project trains supervised learning models to predict whether a student will answer a question correctly.

Models include:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

### 4. Student Clustering

The project groups students based on learning behavior, such as accuracy, progress, activity level, topic diversity, and difficulty exposure.

### 5. Recommendation System

The project creates simple recommendation strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

These strategies simulate how an AI tutor might select the next learning activity.

### 6. Reinforcement Learning Tutor

The project includes a simple Q-learning tutor simulation.

The tutor chooses between easy, medium, and hard questions and receives rewards based on student performance.

This is compared against a random tutor policy.

### 7. Evaluation and Visualization

The project evaluates supervised models, clustering, recommendation examples, and reinforcement learning policies.

It also generates result tables and plots for easier interpretation.

### 8. Streamlit Demo

The project includes a Streamlit dashboard that displays:

- dataset overview
- supervised model results
- student clustering
- recommendation examples
- reinforcement learning comparison

## Tools and Technologies

- Python
- pandas
- NumPy
- scikit-learn
- matplotlib
- Streamlit
- pytest
- Git / GitHub

## What Makes This Project Strong

This project is stronger than a basic machine learning notebook because it includes:

- complete project structure
- reproducible pipeline
- automated smoke test
- supervised learning
- clustering
- recommendation logic
- reinforcement learning simulation
- result visualizations
- Streamlit demo
- research-style documentation
- ethics and limitations discussion

## Current Limitations

The current version uses synthetic data and a simplified reinforcement learning environment.

It should be understood as a research prototype, not a production-ready educational system.

## Future Improvements

Future versions can include:

- real educational datasets such as ASSISTments or EdNet
- deep knowledge tracing models
- stronger recommendation algorithms
- more realistic reinforcement learning environments
- fairness evaluation
- explainable AI methods
- improved interactive demo

## Resume Bullet

Built an adaptive AI tutor research prototype using Python, scikit-learn, recommendation strategies, clustering, and Q-learning to model student learning behavior, predict answer correctness, and simulate personalized learning decisions.

## LinkedIn Short Post

I built an Adaptive AI Tutor Research Lab project.

The project combines student modeling, supervised learning, clustering, recommendation systems, reinforcement learning, evaluation, visualization, and a Streamlit demo.

The main idea is to explore how an AI tutor can use student interaction history to recommend better learning activities and adapt over time.

This project helped me connect multiple AI/ML concepts into one complete research-style system.

## GitHub Description

Research-style AI/ML project for adaptive learning: knowledge tracing, student clustering, recommendation systems, reinforcement learning tutor simulation, evaluation, visualization, and Streamlit demo.