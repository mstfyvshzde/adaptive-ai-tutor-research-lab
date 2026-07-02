# Ablation Results

## Purpose

This file will record the ablation study results for the Adaptive AI Tutor Research Lab project.

An ablation study tests which parts of the system actually improve performance.

The goal is to understand not only whether the system works, but why it works.

## Why Ablation Matters

A strong research project should not only report final results.

It should also analyze which components are useful.

For this project, ablation helps answer:

- Does student history improve prediction?
- Does question difficulty matter?
- Does weak-topic detection improve recommendations?
- Do clustering features help?
- Does reward shaping improve the RL policy?
- Which part of the system contributes most?

## Planned Ablation Tests

## 1. Without Student History

### Goal

Test whether historical student performance improves the model.

### Removed Features

- Student accuracy so far
- Recent accuracy
- Previous correctness
- Rolling accuracy

### Expected Insight

If performance drops, student history is important for prediction and recommendation.

### Status

Not run yet.

---

## 2. Without Question Difficulty

### Goal

Test whether question difficulty improves learning predictions and recommendations.

### Removed Features

- Question accuracy rate
- Question difficulty estimate
- Question attempt count

### Expected Insight

If performance drops, difficulty is important for adaptive tutoring.

### Status

Not run yet.

---

## 3. Without Weak-Topic Signal

### Goal

Test whether identifying weak topics improves recommendation quality.

### Removed Features

- Topic-level accuracy
- Weak-topic label
- Topic mastery estimate

### Expected Insight

If performance drops, weak-topic detection is important for personalized learning.

### Status

Not run yet.

---

## 4. Without Clustering Features

### Goal

Test whether student behavior clusters improve recommendation or RL policy performance.

### Removed Features

- Student cluster label
- Cluster-level behavior profile

### Expected Insight

If performance improves or does not change, clustering may not be necessary.

If performance drops, learner behavior groups are useful.

### Status

Not run yet.

---

## 5. Without Reward Shaping

### Goal

Test whether a richer reward function improves reinforcement learning performance.

### Compared Reward Functions

Simple reward:

Correct answer = +1  
Wrong answer = 0  

Shaped reward:

Correct answer = +1  
Weak-topic improvement = bonus  
Too easy question = penalty  
Too difficult question = penalty  

### Expected Insight

If shaped reward performs better, reward design is important for adaptive tutoring.

### Status

Not run yet.

---

## Ablation Results Table

| Ablation Test | Main Metric | Result | Interpretation |
|---|---:|---|---|
| Full System | Not run yet | Not run yet | Reference system |
| Without Student History | Not run yet | Not run yet | Pending |
| Without Question Difficulty | Not run yet | Not run yet | Pending |
| Without Weak-Topic Signal | Not run yet | Not run yet | Pending |
| Without Clustering Features | Not run yet | Not run yet | Pending |
| Without Reward Shaping | Not run yet | Not run yet | Pending |

## Notes

No result should be written here until real experiments are completed.

This file will be updated after the supervised models, recommender baselines, and RL policy experiments are implemented.

The final report should use this ablation study to explain which parts of the system matter most.
