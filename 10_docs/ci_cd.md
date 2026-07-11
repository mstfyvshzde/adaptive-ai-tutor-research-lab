# CI/CD Notes

## 1. Overview

This document explains the CI/CD setup for the Adaptive AI Tutor Research Lab.

CI/CD means Continuous Integration and Continuous Delivery or Deployment.

In this project, the current focus is Continuous Integration.

## 2. Why CI Matters

CI helps check whether the project still works after changes.

Instead of only testing the project locally, GitHub can automatically run the pipeline and tests.

This improves reliability and makes the repository more professional.

## 3. Current CI Workflow

The CI workflow is defined in:

`.github/workflows/ci.yml`

The workflow runs when code is pushed to the main branch or when a pull request is opened.

## 4. CI Steps

The workflow performs these steps:

1. Checkout repository
2. Set up Python
3. Install dependencies
4. Run the full pipeline
5. Run tests

Main commands used by CI:

`python run_pipeline.py`

`pytest`

## 5. What CI Checks

The CI workflow checks that:

- dependencies can be installed
- the full ML pipeline runs
- output files can be generated
- automated tests pass

This helps catch errors early.

## 6. Relationship With Local Testing

Before pushing changes, the project should still be tested locally.

Recommended local commands:

`python run_pipeline.py`

`pytest`

The CI workflow repeats these checks on GitHub.

## 7. Current Limitations

Current CI limitations:

- it uses synthetic data only
- it does not deploy the Streamlit app
- it does not test real datasets
- it does not perform long-running experiments
- it does not check model fairness

These limitations are acceptable for the current research prototype.

## 8. Future CI Improvements

Future improvements may include:

- code style checks
- linting
- type checking
- notebook checks
- documentation checks
- real dataset preprocessing tests
- Streamlit smoke test
- deployment workflow

## 9. Summary

The CI setup makes the project more reliable.

It shows that the pipeline and tests can run automatically, not only manually on a local machine.