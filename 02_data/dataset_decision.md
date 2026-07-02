# Dataset Decision

## Primary Dataset

The primary dataset for this project will be EdNet-KT1.

EdNet is a large-scale educational dataset collected from a real AI tutoring service.  
It contains student-question interaction data that is suitable for knowledge tracing, recommendation, and adaptive learning experiments.

## Why EdNet-KT1?

EdNet-KT1 is selected because it provides the core data needed for the first version of the Adaptive AI Tutor:

- Student interaction history
- Question-solving logs
- Timestamps
- Question IDs
- User answers
- Elapsed time

This makes it suitable for:

- Supervised knowledge tracing
- Student behavior analysis
- Recommendation baselines
- Reinforcement learning environment design

## Backup Dataset

ASSISTments will be kept as a backup dataset.

If EdNet is too large or difficult to process at the beginning, ASSISTments can be used for faster prototyping.

## Dataset Strategy

The project will not start with the full dataset immediately.

The first version will use a small sample of EdNet-KT1 to build and test the full pipeline.

The pipeline will include:

1. Data loading
2. Data cleaning
3. Feature engineering
4. Supervised prediction
5. Recommendation baseline
6. RL environment simulation

After the pipeline works on a small sample, the project can scale to a larger subset.

## Initial Dataset Plan

### Phase 1

Use a small sample of students from EdNet-KT1.

### Phase 2

Build the complete preprocessing and modeling pipeline.

### Phase 3

Scale the experiment to a larger dataset subset.

### Phase 4

Compare results across baselines and RL policies.

## Notes

The first goal is not to process the largest possible dataset.

The first goal is to build a clean, reproducible, research-style pipeline that can later scale.