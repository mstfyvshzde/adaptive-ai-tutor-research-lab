# Reproducibility and Ethics Note

## Reproducibility

This project is designed to be reproducible from a clean environment.

To run the full pipeline:

    python run_pipeline.py

This command runs:

1. demo dataset creation
2. dataset validation
3. feature engineering
4. supervised baseline models
5. student behavior clustering
6. recommendation baselines
7. reinforcement learning environment
8. Q-learning agent
9. policy comparison
10. result visualizations

To run the Streamlit demo:

    streamlit run 07_demo/app.py

To run tests:

    pytest

## AI-Assisted Development Disclosure

AI tools were used as coding assistance during this project.

The assistance was mainly used for:

- boilerplate code generation
- file structure organization
- debugging support
- documentation drafting
- experiment pipeline scaffolding

The project design, learning goals, experiment direction, result interpretation, and final research framing were reviewed and adapted by the author.

This project should be understood as an AI-assisted research portfolio project, not as a claim that every line of code was manually written from scratch.

## Author Responsibility

The author is responsible for:

- understanding the system architecture
- running and testing the code
- explaining the main methods
- interpreting the results
- identifying limitations
- improving the project over time

## Limitations

This project currently uses a synthetic demo dataset.

The results are useful for testing the pipeline, but they should not be interpreted as real-world educational impact.

Future work should evaluate the system on real student interaction datasets such as EdNet or ASSISTments.

## Summary

This project demonstrates a reproducible AI tutoring pipeline that combines:

- knowledge tracing
- student profiling
- recommender systems
- reinforcement learning
- evaluation and visualization