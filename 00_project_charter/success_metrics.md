# Success Metrics

## Purpose

This document defines how the success of the Adaptive AI Tutor project will be measured.

The project is not only a software implementation.  
It is an AI + education + learning science research project.

Because of this, success will be measured from multiple perspectives:

- Prediction quality
- Recommendation quality
- Learning improvement
- Reinforcement learning performance
- Explainability
- Research quality
- Product usefulness

---

## 1. Supervised Learning Metrics

The supervised model will predict whether a student is likely to answer the next question correctly.

### Metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Log Loss

### Success Target

The supervised model should perform better than a simple majority-class baseline.

The goal is not only high accuracy, but also reliable probability prediction.

---

## 2. Student Behavior Analysis Metrics

The clustering component will group students based on learning behavior.

### Metrics

- Cluster interpretability
- Silhouette score
- Student behavior separation
- Visualization quality

### Success Target

The project should identify meaningful learner groups, such as:

- Strong and consistent learners
- Fast but inconsistent learners
- Slow but improving learners
- Struggling learners

---

## 3. Recommendation Metrics

The recommender system will suggest the next learning activity.

### Metrics

- Recommendation success rate
- Weak-topic improvement
- Average predicted learning gain
- Comparison against random recommendation
- Comparison against difficulty-based recommendation

### Success Target

The recommendation system should perform better than random and simple rule-based baselines.

---

## 4. Reinforcement Learning Metrics

The RL tutor policy will optimize long-term learning paths.

### Metrics

- Cumulative reward
- Average reward per episode
- Learning gain
- Mastery improvement
- Regret
- Policy comparison

### Success Target

The RL-based policy should outperform at least one major baseline in long-term learning-related metrics.

---

## 5. Ablation Study Metrics

Ablation analysis will test which parts of the system matter most.

### Components to Test

- Without student history
- Without question difficulty
- Without clustering features
- Without weak-topic signal
- Without reward shaping

### Success Target

The project should clearly show which system components improve or reduce performance.

---

## 6. Explainability Metrics

The tutor should not only recommend an activity, but also explain why.

### Evaluation Criteria

- Can the system explain the recommendation?
- Is the explanation understandable?
- Does the explanation connect to student weakness or mastery?
- Is the recommendation transparent enough for a learner?

### Success Target

Each recommendation should include a short explanation, such as:

"The student is weak in algebra and recently answered easy algebra questions correctly, so the system recommends a medium-difficulty algebra question."

---

## 7. Research Quality Metrics

The final project should look like a serious research artifact.

### Criteria

- Clear research question
- Clear hypothesis
- Dataset explanation
- Multiple baselines
- Experiment logs
- Visualizations
- Final comparison table
- Limitations section
- Future work section

### Success Target

The project should be understandable and impressive to both technical and non-technical reviewers.

---

## 8. Portfolio Quality Metrics

The final GitHub repository should show professional-level work.

### Criteria

- Clean folder structure
- Clear README
- Reproducible code
- Well-named notebooks
- Saved figures and tables
- Research report
- Demo screenshots
- LinkedIn-ready summary

### Success Target

A reviewer should be able to understand the project goal, methods, results, and contribution within a few minutes.