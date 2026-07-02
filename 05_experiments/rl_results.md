# Reinforcement Learning Results

## Purpose

This file will record the reinforcement learning results for the Adaptive AI Tutor Research Lab project.

The goal of the RL component is to test whether an adaptive tutor policy can improve learning paths compared to simpler recommendation baselines.

## RL Research Question

Can a reinforcement learning-based tutor policy improve long-term learning outcomes compared to random, difficulty-based, weak-topic, and supervised recommender baselines?

## Planned RL Methods

The first version will test simple and interpretable RL methods before moving to deep reinforcement learning.

Planned methods:

- Random policy
- Multi-armed bandit
- Contextual bandit
- Q-learning
- Deep Q-Network as optional extension

## Environment Design

The RL tutor environment will include:

### State

The learner's current situation.

Possible state features:

- Recent accuracy
- Topic-level mastery
- Attempt count
- Weak-topic signal
- Current difficulty level
- Previous correctness
- Student cluster

### Action

The next tutoring decision.

Possible actions:

- Recommend easy question
- Recommend medium question
- Recommend hard question
- Review weak topic
- Continue current topic
- Switch topic

### Reward

The learning feedback signal.

Possible reward signals:

- Correct answer
- Mastery improvement
- Weak-topic improvement
- Penalty for questions that are too easy
- Penalty for questions that are too difficult

## Planned Metrics

RL performance will be evaluated using:

- Cumulative reward
- Average reward per episode
- Learning gain
- Mastery improvement
- Weak-topic improvement
- Regret
- Comparison against baselines

## Results Table

| Method | Cumulative Reward | Learning Gain | Mastery Improvement | Notes |
|---|---:|---:|---:|---|
| Random Policy | Not run yet | Not run yet | Not run yet | Baseline |
| Bandit Policy | Not run yet | Not run yet | Not run yet | Planned |
| Contextual Bandit | Not run yet | Not run yet | Not run yet | Planned |
| Q-Learning | Not run yet | Not run yet | Not run yet | Planned |
| DQN | Not run yet | Not run yet | Not run yet | Optional |

## Notes

No final result should be added until real experiments are completed.

This file will be updated after the RL environment and training pipeline are implemented.
