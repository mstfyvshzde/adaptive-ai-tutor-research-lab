# Recommendation System Model Card

## 1. System Purpose

This model card describes the recommendation system component of the Adaptive AI Tutor Research Lab.

The goal of this component is to recommend learning activities based on student performance, question difficulty, and weak topics.

## 2. Task

The task is educational recommendation.

The system selects a question or learning activity that may be useful for a student.

The current version focuses on simple baseline recommendation strategies.

## 3. Recommendation Strategies

The project currently includes three recommendation strategies:

### 1. Random Recommendation

Selects a question randomly.

This is used as a simple baseline.

### 2. Difficulty-Based Recommendation

Selects a question difficulty based on recent student accuracy.

Example logic:

- low recent accuracy → easier question
- medium recent accuracy → medium question
- high recent accuracy → harder question

### 3. Weak-Topic Recommendation

Finds the topic where the student has the lowest performance and recommends a question from that topic.

This strategy is designed to help students practice weaker areas.

## 4. Input Data

The recommendation system uses engineered student learning features such as:

- student ID
- question ID
- topic tag
- difficulty level
- recent accuracy
- topic-level accuracy
- student performance history

## 5. Output

The system outputs recommendation examples.

Each recommendation includes:

- student ID
- recommendation strategy
- recommended question ID
- recommended topic
- recommended difficulty
- explanation reason

## 6. Intended Use

This component is intended for:

- educational AI prototyping
- adaptive learning experimentation
- comparing simple recommendation strategies
- supporting the reinforcement learning tutor simulation

## 7. Not Intended Use

This system should not be used as a final real-world tutoring system.

It should not be used to:

- replace teacher judgment
- force students into fixed learning paths
- make high-stakes educational decisions
- label students permanently based on weak topics
- decide official academic outcomes

## 8. Evaluation

The current recommendation system is a baseline component.

It creates interpretable recommendation examples but does not yet use advanced recommender evaluation metrics.

Future evaluation may include:

- recommendation accuracy
- learning gain
- engagement improvement
- topic mastery improvement
- comparison with real student outcomes

## 9. Limitations

Current limitations:

- recommendations are rule-based
- data is synthetic
- student behavior is simulated
- no real learning outcome is measured
- no long-term student progress is tracked
- no user feedback loop is included

## 10. Ethical Considerations

Educational recommendation systems must be designed carefully.

Important concerns include:

- avoiding unfair recommendations
- protecting student data
- explaining why a recommendation was made
- avoiding negative labels such as weak student
- keeping teachers and learners involved
- avoiding over-reliance on automation

## 11. Future Improvements

Future improvements may include:

- collaborative filtering
- content-based recommendation
- hybrid recommendation systems
- deep learning recommendation models
- real educational datasets
- feedback-based recommendation updates
- explainable recommendation outputs
- fairness evaluation

## 12. Summary

The recommendation system is a simple but important part of the adaptive tutor pipeline.

It connects student modeling with tutoring decisions by answering this question:

What should the student practice next?