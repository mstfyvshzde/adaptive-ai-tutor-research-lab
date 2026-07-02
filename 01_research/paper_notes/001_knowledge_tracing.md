# Paper Note 001 — Knowledge Tracing

## Topic

Knowledge Tracing

## Purpose of This Note

This note explains the role of knowledge tracing in the Adaptive AI Tutor Research Lab project.

Knowledge tracing is one of the core ideas behind adaptive learning systems. It focuses on estimating a learner's knowledge state over time by analyzing their learning history.

In this project, knowledge tracing will help the AI tutor understand what a student probably knows, what they are struggling with, and what learning activity should come next.

## Core Idea

A student answers a sequence of questions.

Each answer provides information about the student's current knowledge.

The system uses this interaction history to estimate:

- Which concepts the student understands
- Which concepts are weak
- Whether the student is improving
- Whether the next question should be easier, similar, or harder
- Whether the student is ready to move to a new topic

The goal is not only to count correct and incorrect answers.

The goal is to model learning progress over time.

## Simple Example

A student answers five algebra questions:

Q1: correct  
Q2: correct  
Q3: wrong  
Q4: correct  
Q5: wrong  

A simple system may only calculate accuracy:

3 correct out of 5 = 60% accuracy

A knowledge tracing system asks deeper questions:

Is the student improving?  
Are the mistakes connected to one concept?  
Were the wrong questions harder?  
Did the student spend too much or too little time?  
Should the next activity review the weak concept?

This makes knowledge tracing useful for personalized learning.

## Connection to This Project

The Adaptive AI Tutor will use knowledge tracing to predict:

Will the student answer the next question correctly?

This prediction will support later parts of the system:

- Student modeling
- Weak-topic detection
- Recommendation
- Reinforcement learning state design
- Learning path optimization
- Explanation of tutoring decisions

Knowledge tracing is the first major modeling layer of the project.

## Input Data

The system will use student-question interaction data.

Possible raw inputs:

- Student ID
- Question ID
- Timestamp
- User answer
- Correct answer
- Elapsed time
- Question topic
- Skill tag
- Question difficulty

Possible engineered inputs:

- Student accuracy so far
- Student recent accuracy
- Student topic-level accuracy
- Number of previous attempts
- Previous answer correctness
- Average response time
- Question historical accuracy
- Estimated question difficulty
- Time since previous question

## Target Variable

The main target variable will be:

`is_correct`

Definition:

`is_correct = 1 if user_answer == correct_answer`  
`is_correct = 0 otherwise`

The supervised learning model will try to predict this value for future student-question interactions.

## Output

The main output of the knowledge tracing model will be:

`P(correct_next_question)`

This means the estimated probability that a student will answer the next question correctly.

Example:

Student: 1042  
Question: 381  
Predicted probability of correct answer: 0.73

This probability can help the tutor decide whether the question is suitable for the student.

## Why Knowledge Tracing Matters

Knowledge tracing is important because adaptive tutoring requires an estimate of the learner's current state.

Without knowledge tracing, the tutor may recommend questions randomly or based only on general difficulty.

With knowledge tracing, the tutor can make more personalized decisions.

Instead of asking:

Which question is popular?

The tutor asks:

What does this student need right now?

This is the foundation of adaptive learning.

## Baseline Approach

The first version of this project will treat knowledge tracing as a supervised learning problem.

The model will predict whether a student will answer a question correctly using historical and question-level features.

Planned baseline models:

- Logistic Regression
- Random Forest
- Gradient Boosting
- Neural Network baseline as optional extension

The first goal is not to start with the most complex model.

The first goal is to build a clean, understandable, and reproducible pipeline.

## Why Not Start with Deep Learning?

Deep learning can be powerful for knowledge tracing, especially when modeling long sequences of student interactions.

However, this project will not start with deep learning as the main method.

Reasons:

- Simpler models are easier to debug
- Simpler models are easier to explain
- Feature importance is easier to analyze
- Baselines are necessary before advanced models
- The full research pipeline should work before adding complexity

Deep Knowledge Tracing can be added later as an advanced extension.

## Important Concepts

### Knowledge State

The estimated understanding level of a student at a specific moment.

### Mastery

The idea that a student has learned a specific skill or concept.

### Learning Sequence

The ordered history of a student's learning interactions.

Example:

Question 1 → Question 2 → Question 3 → Question 4

### Skill Tag

A label that connects a question to a concept or topic.

Example:

question_id: 142  
tag: algebra

### Correctness Prediction

The task of predicting whether the student will answer a future question correctly.

## Role in the Full System

Knowledge tracing will provide the student state used by later components.

The planned pipeline:

Student history  
↓  
Knowledge tracing model  
↓  
Estimated knowledge state  
↓  
Recommendation system  
↓  
RL tutor policy  
↓  
Next learning activity

This makes knowledge tracing one of the most important foundations of the project.

## Evaluation Metrics

The supervised knowledge tracing model will be evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Log Loss

ROC-AUC and Log Loss are especially important because the tutor needs reliable probability estimates, not only correct class labels.

## Data Leakage Risk

Data leakage is a serious risk in knowledge tracing.

The model must not use future information when predicting a student's current or next answer.

Important rules:

- Student history must be sorted by timestamp
- Features must be calculated only from previous interactions
- Future correctness must not be included in current features
- Train and test splits should respect time or student separation
- Question statistics should be calculated carefully to avoid leaking test data

Avoiding data leakage is essential for making the results trustworthy.

## Expected Features for First Model

The first model may use these features:

- student_attempt_count
- student_accuracy_so_far
- student_recent_accuracy
- student_avg_elapsed_time
- question_accuracy_rate
- question_attempt_count
- question_difficulty
- previous_correct
- previous_elapsed_time
- rolling_accuracy_5
- rolling_accuracy_10

These features are simple but meaningful.

They help the model understand both the student and the question.

## Expected Result

The knowledge tracing model should perform better than a simple baseline.

Simple baseline example:

Always predict the majority class

A stronger model should use student history and question information to make more accurate predictions.

The project should compare models clearly and report both strengths and limitations.

## Limitations

Knowledge tracing predictions may be imperfect.

Possible limitations:

- A correct answer does not always mean true understanding
- A wrong answer may happen because of a careless mistake
- Response time can be noisy
- Skill tags may be incomplete
- Some students may have too little history
- Question difficulty may change depending on the student
- The model may not understand motivation, fatigue, or external factors

These limitations should be discussed in the final research report.

## Design Decision for This Project

The first version of knowledge tracing will be implemented with supervised machine learning.

The model will use engineered features from student history and question metadata.

Later extensions may include:

- Deep Knowledge Tracing
- Sequence models
- Transformer-based student modeling
- Cognitive diagnosis models

This keeps the project realistic while leaving space for advanced future work.

## Notes for Implementation

Implementation priorities:

1. Load student-question interaction data
2. Sort interactions by student and timestamp
3. Join question metadata
4. Create the `is_correct` target
5. Build historical features without data leakage
6. Train baseline models
7. Evaluate with multiple metrics
8. Save results and plots
9. Document findings clearly

## Why This Makes the Project Stronger

Knowledge tracing gives the project an educational research foundation.

This project is not only about software.

It is about understanding learning behavior and designing an AI system that can support students across different fields.

Knowledge tracing connects the technical model to the real educational goal:

Help each learner study the right thing at the right time.