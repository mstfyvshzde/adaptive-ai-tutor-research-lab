# Adaptive AI Tutor Research Lab

Adaptive AI Tutor Research Lab is a research-style AI/ML portfolio project that explores how an intelligent tutoring system can personalize learning using student modeling, supervised learning, clustering, recommendation strategies, and reinforcement learning.

The project builds a complete end-to-end pipeline:

data generation → validation → feature engineering → supervised prediction → clustering → recommendation → reinforcement learning → evaluation → visualization → demo

## Project Goal

The main goal is to investigate how an AI tutor can use student interaction history to make better personalized learning decisions.

The tutor prototype is designed to answer questions such as:

- Can we predict whether a student will answer correctly?
- Can we group students by learning behavior?
- Can we recommend better learning activities based on student weaknesses?
- Can a reinforcement learning tutor perform better than a random policy?

## Why This Project Matters

Many educational platforms collect student interaction data, but the key challenge is turning that data into useful learning decisions.

This project demonstrates how different AI/ML methods can be connected into one adaptive learning pipeline.

It is not only a model-training notebook. It includes:

- structured project architecture
- reproducible pipeline
- automated testing
- supervised learning baselines
- clustering analysis
- recommendation logic
- reinforcement learning simulation
- visualizations
- Streamlit demo
- research-style documentation
- ethics and limitations discussion

## Current Version

The current version uses synthetic student interaction data.

Synthetic data is used to:

- avoid privacy risks
- make the project reproducible
- test the full pipeline safely
- create a clean research prototype before using real datasets

Future versions can extend the project with real educational datasets such as ASSISTments or EdNet.

## Main Components

### 1. Synthetic Student Learning Data

The project creates demo student interaction data with:

- students
- questions
- topics
- difficulty levels
- elapsed time
- correctness labels

### 2. Feature Engineering

Raw interactions are transformed into learning features such as:

- student accuracy so far
- previous correctness
- rolling accuracy
- topic-level accuracy
- question-level accuracy
- elapsed time
- question difficulty

### 3. Supervised Knowledge Tracing

The supervised learning task predicts whether a student will answer a question correctly.

Models included:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Log Loss

### 4. Student Clustering

Students are grouped based on learning behavior, including:

- total attempts
- final accuracy
- average elapsed time
- topic diversity
- recent accuracy
- progress trend

### 5. Recommendation System

The project includes simple recommendation strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

These strategies simulate how an AI tutor might select the next activity.

### 6. Reinforcement Learning Tutor

A simple Q-learning tutor is implemented.

The tutor observes a student state, chooses an action, receives reward, and learns which question difficulty may work better.

Actions:

- easy question
- medium question
- hard question

The Q-learning tutor is compared against a random policy.

### 7. Evaluation and Visualization

The project generates result tables and plots for:

- supervised model comparison
- student clustering
- recommendation examples
- reinforcement learning policy comparison

### 8. Streamlit Demo

The project includes a Streamlit dashboard that displays:

- dataset overview
- supervised model results
- clustering results
- recommendation examples
- reinforcement learning comparison

## Project Structure

```bash
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
├── 07_demo/
├── 08_report/
├── 09_portfolio_assets/
├── 10_docs/
├── tests/
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## How to Run the Project

### 1. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full pipeline

```bash
python run_pipeline.py
```

### 4. Run tests

```bash
pytest
```

### 5. Launch Streamlit demo

```bash
streamlit run 07_demo/app.py
```

## Expected Outputs

The pipeline creates outputs such as:

- processed feature dataset
- supervised model metrics
- student cluster summaries
- recommendation examples
- reinforcement learning results
- comparison tables
- visualization plots

Example output folders:

```bash
06_results/tables/
06_results/figures/
07_demo/demo_data/
```

## Technologies Used

- Python
- pandas
- NumPy
- scikit-learn
- matplotlib
- Streamlit
- pytest
- Git / GitHub

## Limitations

Current limitations:

- dataset is synthetic
- student behavior is simulated
- reinforcement learning environment is simplified
- recommendations are basic
- no real classroom feedback is used
- no long-term learning outcomes are measured

This project should be understood as a research prototype, not a production-ready educational platform.

## Future Work

Future improvements may include:

- real educational datasets
- deep knowledge tracing models
- stronger recommender systems
- more realistic reinforcement learning environments
- fairness evaluation
- explainable AI methods
- improved interactive tutor demo

## Research and Ethics

The project includes documentation on reproducibility, privacy, limitations, and responsible use.

AI tutoring systems should support students and teachers, not replace human judgment or make high-stakes educational decisions automatically.

## Portfolio Summary

This project demonstrates the ability to connect multiple AI/ML ideas into one complete system:

- data engineering
- feature engineering
- supervised learning
- unsupervised learning
- recommender systems
- reinforcement learning
- evaluation
- visualization
- testing
- documentation
- demo deployment readiness

## Status

Current status: working research prototype with full pipeline, test coverage, result generation, and Streamlit demo.