# Adaptive AI Tutor Research Lab

A research-style AI project that simulates an adaptive tutoring system using:

- knowledge tracing
- student behavior clustering
- recommendation baselines
- reinforcement learning
- evaluation and visualization

The goal is to study how an AI tutor can estimate a student's learning state and recommend better next learning activities over time.

## Project Idea

Traditional learning platforms often give the same content to every student.

This project explores a different approach:

The tutor observes student performance, builds learning features, groups students into behavior profiles, recommends next questions, and tests reinforcement learning policies for adaptive decision-making.

## Core Research Question

Can an adaptive AI tutor improve learning recommendations by combining student knowledge features, recommender systems, and reinforcement learning?

## Main Components

1. Demo Dataset Creation  
   Creates a synthetic student-learning dataset for testing the full pipeline.

2. Feature Engineering  
   Builds student history, topic performance, question difficulty, and rolling accuracy features.

3. Supervised Knowledge Tracing  
   Trains baseline models to predict whether a student will answer correctly.

4. Student Clustering  
   Groups students into learner profiles based on behavior.

5. Recommendation Baselines  
   Recommends questions using random, difficulty-based, and weak-topic strategies.

6. Reinforcement Learning  
   Simulates a tutoring environment and compares random policy with Q-learning.

7. Visualization and Demo  
   Generates result plots and provides a Streamlit demo app.

## How to Run

Install dependencies:

    pip install -r requirements.txt

Run the full pipeline:

    python run_pipeline.py

Run tests:

    pytest

Run the demo app:

    streamlit run 07_demo/app.py

## Project Structure

    00_project_charter/
    01_research/
    02_data/
    03_notebooks/
    04_src/
    05_experiments/
    06_results/
    07_demo/
    08_report/
    09_portfolio_assets/
    10_docs/
    tests/

## Current Status

The first complete demo pipeline is implemented.

Current features include:

- synthetic demo dataset
- dataset validation
- feature engineering
- supervised baseline models
- student clustering
- simple recommendation baselines
- RL tutor environment
- Q-learning agent
- policy comparison
- result visualizations
- Streamlit demo
- smoke test for the full pipeline

## Reproducibility

The project can be tested with one command:

    python run_pipeline.py

This regenerates the demo data, model results, evaluation tables, and figures.

For more details, see:

    10_docs/reproducibility_and_ethics.md

## Limitations

This version uses a synthetic demo dataset.

The results are useful for testing the architecture and experiment pipeline, but they should not be interpreted as real-world educational impact yet.

Future work should evaluate the system on real student-learning datasets such as EdNet or ASSISTments.

## AI-Assisted Development Note

AI tools were used for coding assistance, boilerplate generation, debugging support, and documentation drafting.

The project design, experiment direction, result interpretation, and final research framing were reviewed and adapted by the author.

## Author

Shahzada Mustafayev