# Paper Note 003 — Recommender Systems in Education

## Topic

Educational Recommender Systems

## Purpose of This Note

This note explains how recommender systems connect to the Adaptive AI Tutor Research Lab project.

A recommender system suggests items to users.

In normal platforms, these items may be movies, songs, products, or posts.

In education, the recommended item is different.

It may be:

- A question
- A topic
- A lesson
- A practice activity
- A review exercise
- A learning path

The goal is not only to recommend what the learner may like.

The goal is to recommend what helps the learner improve.

## Core Idea

Educational recommender systems try to answer this question:

What should the student study next?

This is different from normal recommendation.

A movie recommender may ask:

What will the user enjoy?

An educational recommender should ask:

What will help the learner improve?

This makes educational recommendation more complex and more meaningful.

## Why This Matters

Most students do not know exactly what they should study next.

Some students repeat topics they already know.

Some students jump to difficult topics too early.

Some students avoid weak topics.

Some students need review before moving forward.

A recommender system can help by using data to suggest a better next step.

## Connection to This Project

The Adaptive AI Tutor needs a recommendation layer.

The knowledge tracing model estimates the student's current state.

The recommender system uses that state to suggest the next learning activity.

The reinforcement learning component later tries to improve this recommendation process over time.

The pipeline is:

Student history  
↓  
Knowledge tracing  
↓  
Estimated student state  
↓  
Recommender system  
↓  
Suggested next activity  
↓  
Reinforcement learning policy improvement

## Educational Recommendation vs Normal Recommendation

Normal recommendation often focuses on preference.

Example:

The user liked action movies, so recommend another action movie.

Educational recommendation focuses on learning value.

Example:

The student is weak in algebra and recently solved easy algebra questions correctly, so recommend a medium-difficulty algebra question.

This difference is important.

A good educational recommendation should balance:

- Current skill level
- Weak topics
- Question difficulty
- Learning progress
- Student frustration
- Long-term mastery

## Possible Recommendation Targets

In this project, the system may recommend:

- The next question
- The next topic
- The next difficulty level
- A review activity
- A practice sequence

The first version will likely focus on next-question or next-topic recommendation.

This keeps the system realistic and easier to evaluate.

## Baseline Recommendation Methods

The project should not start directly with a complex recommender.

It should compare multiple baselines.

### 1. Random Recommendation

The system recommends a random question or topic.

This is the weakest baseline.

It helps answer:

Is the model better than chance?

### 2. Difficulty-Based Recommendation

The system recommends questions based on difficulty.

Example:

If the student is weak, recommend easier questions.

If the student is strong, recommend harder questions.

This is simple but useful.

### 3. Weak-Topic Recommendation

The system identifies weak topics and recommends practice from those topics.

Example:

If the student has low accuracy in probability, recommend probability questions.

This is a strong educational baseline.

### 4. Content-Based Recommendation

The system recommends questions similar to topics or skills the student needs.

It uses question metadata such as:

- Tags
- Topic
- Part
- Difficulty
- Skill category

### 5. Collaborative Filtering

The system uses patterns from similar students.

Example:

Students with similar learning histories improved after practicing a certain topic.

This method can be powerful, but it may be harder to use when student data is sparse.

### 6. Supervised Model-Based Recommendation

The system uses the knowledge tracing model to estimate the probability of correctness for possible next questions.

Then it selects questions that are useful for learning.

The goal is not always to choose the easiest question.

A good recommendation may choose a question that is challenging but still realistic.

## Challenge Level

A useful educational recommendation should avoid two extremes.

Too easy:

The student gets the answer correct, but learns little.

Too hard:

The student gets frustrated and may not learn effectively.

The best recommendation is often in the middle.

This is sometimes called the learner's zone of productive challenge.

## How Recommendation Supports Reinforcement Learning

The recommender system provides strong baselines for the RL tutor.

The RL policy should not only be compared against random behavior.

It should be compared against serious recommendation strategies.

This makes the final evaluation more trustworthy.

The main comparison may include:

- Random policy
- Difficulty-based policy
- Weak-topic policy
- Supervised recommender policy
- Reinforcement learning policy

If RL performs better than these baselines, the project becomes much stronger.

## Input Features

The recommender system may use:

- Student accuracy so far
- Student recent accuracy
- Topic-level mastery
- Question difficulty
- Question tags
- Previous mistakes
- Response time
- Similar student behavior
- Predicted probability of correctness

These features connect recommendation to knowledge tracing and student behavior analysis.

## Output

The recommender system should output a recommended activity.

Example:

Recommended activity: Algebra Question 245  
Difficulty: Medium  
Reason: The student is weak in algebra but recently solved easy algebra questions correctly.

This output should be understandable, not only numerical.

## Explainability

Explainability is important in educational recommendation.

The system should explain why it recommends something.

Example explanation:

The student has low mastery in geometry.  
The previous geometry questions were difficult for the student.  
The system recommends an easier geometry question to rebuild confidence and improve mastery.

This makes the tutor more useful for learners and teachers.

## Evaluation

Educational recommenders are difficult to evaluate because the true goal is learning improvement.

Possible evaluation metrics:

- Recommendation success rate
- Weak-topic improvement
- Predicted learning gain
- Mastery improvement
- Comparison against random baseline
- Comparison against difficulty-based baseline
- Student cluster-level performance

The project should evaluate whether recommendations actually support learning-related goals.

## Data Leakage Risk

Recommendation systems can also suffer from data leakage.

The system must not use future performance when making a recommendation.

Important rules:

- Use only past student history
- Use only available question metadata
- Avoid using future correctness
- Split data carefully
- Calculate question statistics from training data only when needed

This is important for trustworthy evaluation.

## Limitations

Educational recommender systems have limitations.

Possible limitations:

- The system may recommend based on incomplete data
- Some students may have very little history
- Question tags may be noisy
- Correctness may not fully represent learning
- Response time may not reflect true effort
- Recommendations may be too narrow if they only focus on weak topics
- A useful learning path may require human educational judgment

These limitations should be discussed in the final report.

## Design Decision for This Project

The first version of the project will build several recommender baselines before reinforcement learning.

This is important because RL must be compared against meaningful alternatives.

The first recommender systems should be simple, interpretable, and easy to evaluate.

Planned order:

1. Random recommendation
2. Difficulty-based recommendation
3. Weak-topic recommendation
4. Content-based recommendation
5. Supervised model-based recommendation

Collaborative filtering can be added if the dataset structure supports it well.

## Role in the Full Project

The recommender system is the bridge between prediction and action.

Knowledge tracing predicts student performance.

Recommendation decides what to show next.

Reinforcement learning improves this decision over time.

Together, these components create an adaptive tutor.

## Why This Makes the Project Stronger

This project becomes stronger because it does not only predict student correctness.

It uses prediction to make learning decisions.

That makes the project more realistic and more valuable.

The final system should not only answer:

Can we predict performance?

It should answer:

Can we use AI to guide learning better?