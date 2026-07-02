# Baseline Results

## Purpose

This file will record the baseline results for the Adaptive AI Tutor Research Lab project.

Baselines are important because the reinforcement learning tutor must be compared against simpler and more interpretable methods.

The goal is not only to build an advanced model.

The goal is to prove whether the advanced model is actually better than strong baselines.

---

## Why Baselines Matter

A project becomes stronger when it compares multiple methods fairly.

If the RL tutor only performs better than random recommendation, the result is weak.

If the RL tutor performs better than meaningful educational baselines, the result becomes much stronger.

Baselines help answer:

- Is the model better than chance?
- Is the model better than simple rules?
- Is the model better than supervised prediction?
- Is reinforcement learning necessary?
- Which method gives the best learning-related outcome?

---

## Planned Baselines

## 1. Majority-Class Baseline

### Purpose

Used for supervised knowledge tracing.

This baseline always predicts the most common class.

Example:

If most answers are correct, the model predicts correct for every interaction.

### Why It Matters

Any supervised model should perform better than this baseline.

### Metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Log Loss

### Status

Not started yet.

---

## 2. Random Recommendation Baseline

### Purpose

Used for recommendation and RL comparison.

The system randomly selects the next question or topic.

### Why It Matters

This is the weakest recommendation baseline.

Every serious recommendation method should perform better than random selection.

### Metrics

- Recommendation success rate
- Average learning gain
- Weak-topic improvement
- Cumulative reward

### Status

Not started yet.

---

## 3. Difficulty-Based Baseline

### Purpose

The system recommends questions based on estimated difficulty.

Example:

- Weak student → easier question
- Medium student → medium question
- Strong student → harder question

### Why It Matters

Difficulty-based recommendation is simple but educationally meaningful.

It tests whether adapting difficulty alone can improve learning decisions.

### Metrics

- Recommendation success rate
- Learning gain
- Mastery improvement
- Comparison against random baseline

### Status

Not started yet.

---

## 4. Weak-Topic Baseline

### Purpose

The system identifies the learner's weakest topic and recommends more practice from that topic.

Example:

If the student has low accuracy in probability, recommend probability questions.

### Why It Matters

This is one of the strongest simple educational baselines.

It directly targets student weakness.

### Metrics

- Weak-topic improvement
- Topic mastery gain
- Recommendation success rate
- Comparison against random and difficulty-based baselines

### Status

Not started yet.

---

## 5. Content-Based Recommendation Baseline

### Purpose

The system recommends activities using question metadata.

Possible metadata:

- Topic
- Skill tag
- Difficulty
- Part
- Question similarity

### Why It Matters

Content-based recommendation can personalize learning without needing similar-student data.

### Metrics

- Recommendation success rate
- Learning gain
- Weak-topic improvement
- Coverage of recommended topics

### Status

Not started yet.

---

## 6. Supervised Model-Based Recommendation Baseline

### Purpose

The system uses the knowledge tracing model to estimate the probability that a student will answer candidate questions correctly.

Then it recommends a question based on predicted usefulness.

### Why It Matters

This is a strong baseline because it uses the supervised model to guide learning decisions.

The RL policy should be compared against this method.

### Metrics

- Predicted learning gain
- Recommendation success rate
- Mastery improvement
- Comparison against RL policy

### Status

Not started yet.

---

## Baseline Comparison Table

| Method | Purpose | Status | Main Metric | Notes |
|---|---|---|---|---|
| Majority-Class Baseline | Supervised prediction | Not started | Accuracy / Log Loss | Weakest supervised baseline |
| Random Recommendation | Recommendation | Not started | Learning gain | Weakest recommendation baseline |
| Difficulty-Based | Recommendation | Not started | Recommendation success | Simple educational rule |
| Weak-Topic | Recommendation | Not started | Weak-topic improvement | Strong simple baseline |
| Content-Based | Recommendation | Not started | Learning gain | Uses question metadata |
| Supervised Model-Based | Recommendation | Not started | Predicted learning gain | Strong ML-based baseline |

---

## Expected Role in Final Evaluation

The final project should compare the RL tutor against these baselines:

- Random recommendation
- Difficulty-based recommendation
- Weak-topic recommendation
- Content-based recommendation
- Supervised model-based recommendation

The main question:

Does reinforcement learning improve personalized learning decisions compared to simpler methods?

---

## Notes

Baseline results will be updated after experiments are completed.

No result should be written here unless it comes from a real experiment.

This file should remain honest, reproducible, and evidence-based.