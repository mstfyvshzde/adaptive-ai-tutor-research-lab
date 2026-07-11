# Real Dataset Plan

## 1. Overview

This document explains how the Adaptive AI Tutor Research Lab can be extended from synthetic data to real educational datasets.

The current version uses synthetic student interaction data. This is useful for building a safe, reproducible, and complete prototype.

The next research upgrade is to test the pipeline on a real educational dataset.

## 2. Why Real Data Matters

Synthetic data is useful for early development, but real student data is needed to evaluate whether the system works in realistic learning conditions.

Real data can provide:

- real student behavior patterns
- real topic and skill structures
- real response times
- real correctness history
- more realistic difficulty variation
- stronger research credibility

## 3. Candidate Datasets

Possible datasets for future versions:

- ASSISTments
- EdNet
- KDD Cup educational datasets

These datasets are commonly used in educational data mining and knowledge tracing research.

## 4. Target Data Format

The current pipeline expects data in a simple interaction format.

The real dataset should be transformed into columns similar to:

- student_id
- question_id
- timestamp
- tags
- difficulty
- elapsed_time
- is_correct

If the real dataset has different column names, a preprocessing script should map them into this project format.

## 5. Planned Real Dataset Files

Future real dataset support may include:

- `04_src/data/load_real_dataset.py`
- `04_src/data/prepare_real_dataset.py`
- `02_data/external/`
- `02_data/processed/real_features.csv`
- `08_report/appendix/real_data_experiment.md`

## 6. First Real Data Strategy

The first real dataset experiment should be small.

Instead of loading the full dataset immediately, the project should start with a small subset.

Recommended first subset:

- limited number of students
- limited number of questions
- limited number of topics or skills
- cleaned interaction records only

This reduces complexity and makes debugging easier.

## 7. Mapping Real Data to Current Pipeline

The main challenge is converting real dataset columns into the current pipeline structure.

Example mapping:

- user_id → student_id
- item_id or problem_id → question_id
- skill_id or skill_name → tags
- correct → is_correct
- answer_time or response_time → elapsed_time
- timestamp or order_id → timestamp

Not every dataset will have all columns.

Missing columns may need to be estimated or simplified.

## 8. Expected Pipeline Changes

Real data may require changes in:

- data loading
- cleaning
- timestamp handling
- topic mapping
- difficulty estimation
- missing value handling
- feature engineering
- evaluation interpretation

The supervised, clustering, recommendation, and RL parts should reuse as much of the existing pipeline as possible.

## 9. Research Questions for Real Data

Future real data experiments can ask:

- Do supervised models still outperform the dummy baseline?
- Which features matter most on real student data?
- Are student clusters meaningful on real data?
- Do weak-topic recommendations make sense with real skill tags?
- Can the RL simulation be made more realistic using real student behavior?

## 10. Risks

Possible risks:

- dataset is too large
- column names are complex
- skill tags are missing or messy
- timestamps are incomplete
- response time is missing
- difficulty labels are not available
- preprocessing becomes more complex than modeling

Because of this, real dataset integration should be done in a separate phase.

## 11. Success Criteria

The real dataset upgrade is successful if:

- real data can be loaded
- real data can be transformed into the project format
- features can be built without breaking the pipeline
- supervised models can be trained
- results can be compared with synthetic version
- documentation explains the dataset limitations

## 12. Summary

The real dataset upgrade is the next major research step.

The synthetic version proves that the full system works.

The real dataset version will test whether the same pipeline can handle realistic educational data.