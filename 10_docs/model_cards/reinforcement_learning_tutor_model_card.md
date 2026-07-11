# Reinforcement Learning Tutor Model Card

## 1. Model Purpose

This model card describes the reinforcement learning component of the Adaptive AI Tutor Research Lab.

The goal of this component is to simulate how an AI tutor can learn better instructional decisions over time.

The tutor chooses question difficulty levels and receives rewards based on simulated student performance.

## 2. Task

The task is a simplified reinforcement learning decision problem.

The tutor observes a student state, selects an action, receives a reward, and updates its decision strategy.

## 3. Environment

The reinforcement learning environment is a simplified tutoring simulation.

The environment represents a learning session where a tutor recommends questions to a student.

The current environment is not a real classroom environment. It is designed for research prototyping and experimentation.

## 4. State

The tutor state includes simplified student information such as:

- recent accuracy
- weak topic
- current step in the session

These state features help the tutor decide whether to recommend an easy, medium, or hard question.

## 5. Actions

The tutor can choose one of three actions:

- easy question
- medium question
- hard question

Each action represents a tutoring decision about question difficulty.

## 6. Reward

The reward function is based on simulated student performance.

The tutor receives:

- positive reward when the student answers correctly
- small bonus when the question targets the student's weak topic
- small penalty when the question appears too easy or too hard

The reward function is simplified and should be improved in future versions.

## 7. Algorithm

The current version uses Q-learning.

Q-learning is a simple reinforcement learning algorithm that learns a value for each state-action pair.

The agent tries actions, receives rewards, and gradually learns which actions are better in different states.

## 8. Baseline Comparison

The Q-learning tutor is compared against a random policy.

The random policy chooses easy, medium, or hard questions randomly.

The comparison helps answer this question:

Does the learning tutor perform better than random decision-making?

## 9. Evaluation Metrics

The reinforcement learning component is evaluated using:

- average reward
- average correctness
- policy comparison
- reward curve over training episodes

These metrics show whether the tutor is improving in the simulated environment.

## 10. Intended Use

This reinforcement learning tutor is intended for:

- research experimentation
- adaptive learning prototyping
- comparing simple tutor policies
- demonstrating reinforcement learning in education

## 11. Not Intended Use

This component should not be used for real educational decisions.

It should not be used to:

- replace teachers
- grade students
- decide student ability levels
- control real learning paths without human review
- make high-stakes academic decisions

## 12. Data

The reinforcement learning environment uses synthetic student interaction data.

Synthetic data is useful for early development because it avoids privacy risks and makes the project reproducible.

However, synthetic behavior does not fully represent real student learning.

## 13. Limitations

Current limitations:

- the environment is simplified
- student behavior is simulated
- the action space only includes question difficulty
- the reward function is basic
- no real student feedback is used
- long-term learning outcomes are not measured
- the model has not been tested on real educational datasets

## 14. Ethical Considerations

Reinforcement learning in education must be handled carefully.

An RL tutor can influence what a student studies and how difficult the learning path becomes.

Important concerns include:

- student privacy
- fairness
- avoiding harmful recommendations
- avoiding over-automation
- keeping teachers and learners in control
- making tutoring decisions transparent

## 15. Future Improvements

Future versions may include:

- real educational datasets
- richer student states
- more action types
- better reward design
- long-term learning outcome evaluation
- fairness checks
- explainable recommendation logic
- more advanced RL algorithms

## 16. Summary

The reinforcement learning tutor is an experimental component that simulates adaptive tutoring decisions.

It adds a research-oriented layer to the project by testing whether a tutor can learn better decisions than a random policy.