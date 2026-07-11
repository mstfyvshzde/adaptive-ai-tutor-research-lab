# EdNet V2 Methodology

## Overview

V2 extends the Adaptive AI Tutor Research Lab from synthetic data to real educational interaction data.

The purpose of this phase is to evaluate whether the same pipeline design can work with real student-question interactions from EdNet.

## Research Question

Can the adaptive tutor pipeline developed in V1 be applied to real educational interaction data while preserving the same core workflow?

## V1 to V2 Transition

V1 used synthetic student interaction data to prove that the project architecture works end to end.

V2 uses a controlled EdNet subset to test the same idea on real educational data.

## Dataset Strategy

The project will not process the full EdNet dataset.

Instead, it will use a controlled subset with approximately:

- 10,000 students
- 500,000 interactions
- at least 20 interactions per student

This keeps the experiment manageable and reproducible.

## Target Task

The main V2 task is correctness prediction.

The model will use previous student interaction history to predict whether a student will answer a question correctly or incorrectly.

## Planned Pipeline

The V2 pipeline includes:

1. Load EdNet raw data
2. Select a controlled subset
3. Map columns into the project format
4. Validate the mapped dataset
5. Build real-data learning-history features
6. Train supervised baseline models
7. Compare V1 synthetic results with V2 EdNet results
8. Write error analysis and summary

## Why This Matters

Using real educational data makes the project more realistic.

V1 shows that the architecture works.

V2 tests whether the architecture can be applied to real student interaction data.

## Limitations

V2 is still not a production educational platform.

The project does not claim to improve real student learning outcomes yet.

The goal is real-data validation of the machine learning pipeline, not classroom deployment.