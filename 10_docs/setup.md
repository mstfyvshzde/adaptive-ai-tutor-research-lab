# Setup Guide

## 1. Overview

This guide explains how to set up and run the Adaptive AI Tutor Research Lab project locally.

The project includes:

- synthetic data generation
- data validation
- feature engineering
- supervised learning
- student clustering
- recommendation examples
- reinforcement learning simulation
- evaluation
- visualization
- Streamlit demo

## 2. Requirements

Recommended environment:

- Python 3.10 or newer
- Git
- pip
- virtual environment support

## 3. Clone the Repository

```bash
git clone https://github.com/mstfyvshzde/adaptive-ai-tutor-research-lab.git
cd adaptive-ai-tutor-research-lab
```

## 4. Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

## 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run the Full Pipeline

```bash
python run_pipeline.py
```

This command runs the project from start to finish:

1. Create synthetic demo dataset
2. Validate dataset
3. Build features
4. Train supervised baseline models
5. Run student clustering
6. Generate recommendation examples
7. Run reinforcement learning environment
8. Train Q-learning tutor
9. Compare RL policies
10. Create result plots

## 7. Run Tests

```bash
pytest
```

Expected result:

```bash
1 passed
```

This confirms that the full pipeline runs successfully and creates the expected output files.

## 8. Run the Streamlit Demo

```bash
streamlit run 07_demo/app.py
```

The demo dashboard shows:

- dataset overview
- supervised model results
- student clustering results
- recommendation examples
- reinforcement learning comparison

## 9. Important Output Folders

The pipeline creates outputs in these folders:

```bash
02_data/processed/
06_results/tables/
06_results/figures/
07_demo/demo_data/
```

## 10. Common Problems

### Problem: Missing output files

Run:

```bash
python run_pipeline.py
```

### Problem: Streamlit app shows missing file warnings

Run the full pipeline before launching the app:

```bash
python run_pipeline.py
streamlit run 07_demo/app.py
```

### Problem: pytest fails

Run the pipeline manually first:

```bash
python run_pipeline.py
pytest
```

Then read the error message to identify which step failed.

## 11. Development Workflow

Recommended workflow:

```bash
source .venv/bin/activate
python run_pipeline.py
pytest
git status
```

If everything works:

```bash
git add .
git commit -m "Your commit message"
git push
```

## 12. Summary

After setup, the main commands are:

```bash
python run_pipeline.py
pytest
streamlit run 07_demo/app.py
```

These commands run the full project, test it, and open the demo.