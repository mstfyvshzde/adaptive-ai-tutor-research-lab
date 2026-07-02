# Roadmap

## Adaptive AI Tutor Research Lab

This roadmap defines the development plan for the Adaptive AI Tutor project.

The goal is to build a research-style AI system that combines knowledge tracing, recommender systems, student behavior analysis, and reinforcement learning for personalized education.

---

## Week 1 — Research Planning and Dataset Selection

### Goals

- Define the research direction
- Select the final dataset
- Understand the educational AI problem
- Prepare the first research notes

### Tasks

- Finalize problem statement
- Finalize research question
- Finalize hypothesis
- Compare possible datasets
- Select one primary dataset
- Create initial data dictionary
- Start literature review

### Outputs

- Project charter
- Dataset decision
- Research question
- Initial literature notes

---

## Week 2 — Data Exploration and Preprocessing

### Goals

- Understand the raw data
- Clean the dataset
- Build student-question interaction sequences

### Tasks

- Load raw dataset
- Explore columns and missing values
- Analyze student activity
- Analyze question difficulty
- Filter low-quality records
- Build processed dataset
- Save cleaned data

### Outputs

- EDA notebook
- Data preprocessing pipeline
- Data dictionary
- First visualizations

---

## Week 3 — Supervised Knowledge Tracing

### Goals

- Predict whether a student will answer the next question correctly
- Build strong supervised baselines

### Tasks

- Build student-level features
- Build question-level features
- Build history-based features
- Train Logistic Regression
- Train Random Forest
- Train Gradient Boosting
- Compare model performance

### Outputs

- Knowledge tracing notebook
- Model comparison table
- Feature importance plots
- Supervised baseline results

---

## Week 4 — Student Clustering and Recommender Baselines

### Goals

- Discover student learning behavior patterns
- Build next-question recommendation baselines

### Tasks

- Create student behavior features
- Run clustering models
- Visualize student clusters
- Interpret cluster profiles
- Build random recommendation baseline
- Build difficulty-based baseline
- Build weak-topic baseline
- Build supervised recommendation baseline

### Outputs

- Clustering notebook
- Cluster visualization
- Recommender baseline results
- Student behavior analysis

---

## Week 5 — Reinforcement Learning Tutor Environment

### Goals

- Design an RL environment for adaptive tutoring
- Train early RL policies

### Tasks

- Define state space
- Define action space
- Define reward function
- Build tutor simulation environment
- Train bandit policy
- Train Q-learning policy
- Compare RL policies with simple baselines

### Outputs

- RL environment code
- RL training notebook
- Reward curves
- Policy comparison table

---

## Week 6 — Evaluation, Report, and Demo

### Goals

- Complete evaluation
- Prepare final research report
- Build demo application
- Polish GitHub repository

### Tasks

- Create final comparison table
- Run ablation study
- Write limitations
- Create architecture diagram
- Build Streamlit demo
- Add screenshots
- Write final report
- Prepare LinkedIn post
- Clean repository

### Outputs

- Final research report
- Demo app
- GitHub-ready repository
- LinkedIn project summary
- Portfolio assets

---

## Advanced Extensions

These are optional additions if the core project is completed successfully.

- Deep Knowledge Tracing model
- Deep Q-Network agent
- SHAP explainability
- Cold-start student analysis
- Fairness analysis
- Student simulator
- Off-policy evaluation
- Deployment of demo app

---

## Final Deliverables

By the end of the project, the repository should include:

- Clean source code
- Notebooks
- Experiment logs
- Evaluation results
- Figures and tables
- Demo application
- Research-style report
- Portfolio screenshots
- LinkedIn-ready summary