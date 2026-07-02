# Literature Review

## Overview

This literature review supports the Adaptive AI Tutor Research Lab project.

The project is not only a software implementation. It is an AI + education + learning science research project that studies how artificial intelligence can personalize learning paths for students across different fields.

The main focus areas are:

- Knowledge tracing
- Student learning behavior analysis
- Educational recommender systems
- Reinforcement learning for adaptive tutoring
- Explainable AI in education

---

## 1. Intelligent Tutoring Systems

Intelligent Tutoring Systems are educational systems designed to provide personalized instruction, feedback, and learning support.

Traditional learning platforms often present the same content to every learner. Intelligent tutoring systems try to adapt instruction based on the learner's current knowledge, mistakes, progress, and behavior.

For this project, intelligent tutoring systems provide the main research background. The Adaptive AI Tutor is designed to estimate what a learner knows and recommend what they should study next.

### Relevance to This Project

This project uses the idea of adaptive tutoring as the core problem. The system should not only predict performance, but also support better learning decisions over time.

---

## 2. Knowledge Tracing

Knowledge tracing is the task of estimating a student's knowledge state over time based on their interaction history.

A student answers a sequence of questions. The system uses this sequence to estimate whether the student has mastered certain skills or concepts.

In this project, knowledge tracing is used to predict whether a student is likely to answer the next question correctly.

### Relevance to This Project

Knowledge tracing helps the tutor understand the learner's current state.

The supervised learning component will use student history, question difficulty, topic information, and past performance to predict future correctness.

---

## 3. Bayesian Knowledge Tracing

Bayesian Knowledge Tracing is one of the classic approaches to modeling student knowledge.

It represents knowledge as a hidden state and updates the probability that a student has mastered a skill after each interaction.

Although this project may not implement Bayesian Knowledge Tracing in the first version, it is important as a historical and conceptual baseline.

### Relevance to This Project

Bayesian Knowledge Tracing shows that student knowledge can be modeled as something that changes over time.

This idea directly connects to the project's goal of building a dynamic learner model.

---

## 4. Deep Knowledge Tracing

Deep Knowledge Tracing uses neural networks to model student learning sequences.

Instead of manually defining simple mastery probabilities, deep learning models can learn patterns from long sequences of student-question interactions.

This project will not make deep learning the main focus in the first version, because the current project is mainly based on machine learning, recommender systems, and reinforcement learning.

However, Deep Knowledge Tracing can be added later as an advanced extension.

### Relevance to This Project

Deep Knowledge Tracing can become a future upgrade after the basic research pipeline is complete.

For the first version, traditional supervised models will be easier to interpret and compare.

---

## 5. Student Behavior Analysis

Students do not learn in the same way.

Some students are fast and accurate. Some are slow but improving. Some are inconsistent. Some struggle with specific topics.

Student behavior analysis helps identify these patterns using features such as:

- Average accuracy
- Response time
- Improvement rate
- Topic diversity
- Mistake frequency
- Consistency

### Relevance to This Project

The project will use unsupervised learning to cluster students into behavior groups.

This can help answer questions such as:

- Which types of students benefit most from adaptive recommendations?
- Do struggling students need different policies than strong students?
- Can learning behavior improve recommendation quality?

---

## 6. Educational Recommender Systems

Educational recommender systems suggest learning activities such as questions, topics, lessons, or exercises.

Unlike movie or product recommendation, educational recommendation should not only predict what the learner may like. It should recommend what helps the learner improve.

This makes educational recommendation more difficult than simple preference prediction.

### Relevance to This Project

This project will build several recommender baselines, including:

- Random recommendation
- Difficulty-based recommendation
- Weak-topic recommendation
- Content-based recommendation
- Supervised model-based recommendation

These baselines are important because the reinforcement learning model must be compared against simpler methods.

---

## 7. Reinforcement Learning for Adaptive Learning

Reinforcement learning is useful when an agent must make a sequence of decisions.

In this project, the tutor is the agent.

The agent observes the student's current state, chooses the next learning activity, and receives feedback based on student performance or learning improvement.

### Project Formulation

State:

- Student mastery level
- Recent answers
- Topic performance
- Question difficulty
- Learning behavior features

Action:

- Recommend next question
- Recommend next topic
- Increase or decrease difficulty

Reward:

- Correct answer
- Improvement in weak topics
- Mastery gain
- Penalty for questions that are too easy or too difficult

### Relevance to This Project

Reinforcement learning is the main advanced component of the project.

The key research question is whether an RL-based tutor can improve long-term learning paths compared to simpler recommendation strategies.

---

## 8. Explainable AI in Education

In education, explainability is very important.

A student or teacher should understand why the system recommends a specific activity.

A black-box tutor may be difficult to trust, especially if the recommendation affects a student's learning path.

### Relevance to This Project

The final system should explain recommendations in simple language.

Example:

"The student has low mastery in algebra and recently answered easy algebra questions correctly. Therefore, the system recommends a medium-difficulty algebra question."

This makes the project stronger as both an AI system and an educational product.

---

## 9. Research Gap

Many simple machine learning projects focus only on prediction.

However, adaptive learning requires more than prediction.

A strong AI tutor should:

- Understand student knowledge
- Analyze learning behavior
- Recommend useful next activities
- Optimize learning over time
- Explain its decisions
- Compare methods using clear evaluation metrics

This project tries to combine these elements into one research-style system.

---

## 10. How This Literature Review Shapes the Project

The literature review supports the project design in the following way:

Knowledge tracing gives the project a way to model student understanding.

Student behavior analysis gives the project a way to understand different learner types.

Educational recommender systems provide baseline methods for personalized learning.

Reinforcement learning provides a way to optimize learning paths over time.

Explainable AI makes the tutor more understandable and useful.

---

## 11. Initial Research Direction

The first version of the project will focus on building a complete pipeline:

1. Load student-question interaction data
2. Build knowledge tracing features
3. Train supervised models
4. Cluster student behavior
5. Build recommendation baselines
6. Design an RL tutoring environment
7. Compare RL policies against baselines
8. Analyze results
9. Write a final research report

---

## 12. Future Literature Topics

Future versions of this literature review may include deeper notes on:

- Bayesian Knowledge Tracing
- Deep Knowledge Tracing
- Cognitive diagnosis models
- Contextual bandits
- Off-policy evaluation
- Fairness in educational AI
- Human-AI interaction in tutoring systems
- Learning science and mastery learningq