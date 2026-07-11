# Results Summary

## 1. Pipeline Status

The full project pipeline runs successfully.

Main command:

`python run_pipeline.py`

Test command:

`pytest`

Current test result:

`1 passed`

This confirms that the project can generate data, build features, train models, create recommendations, run reinforcement learning, generate plots, and pass the smoke test.

## 2. Dataset Summary

The synthetic demo dataset contains:

- Students: 40
- Questions: 80
- Interactions: 1452
- Average correctness: 0.610

This dataset is used to test the complete adaptive tutor pipeline.

## 3. Supervised Learning Results

The supervised knowledge tracing task predicts whether a student will answer correctly.

Models tested:

- Dummy Classifier
- Logistic Regression
- Random Forest
- Gradient Boosting

Best ROC-AUC result:

- Logistic Regression: 0.9077

Best Accuracy result:

- Logistic Regression and Random Forest: 0.8282

The supervised models perform clearly better than the dummy baseline.

This suggests that the engineered learning-history features contain useful predictive information.

## 4. Clustering Results

The student clustering component groups students based on learning behavior.

Silhouette score:

- 0.238

This score suggests that the clusters show some separation, but they are not extremely strong.

This is expected because the current dataset is synthetic and simplified.

The clustering step is useful as an exploratory analysis of student learning patterns.

## 5. Recommendation Results

The recommendation component creates example tutor recommendations using three strategies:

- random recommendation
- difficulty-based recommendation
- weak-topic recommendation

These strategies are simple baselines.

They help demonstrate how an adaptive tutor can move from prediction to action.

## 6. Reinforcement Learning Results

The reinforcement learning component compares a random policy with a Q-learning tutor.

Random policy:

- Average reward: 0.542
- Average correctness: 0.565

Q-learning tutor:

- Average reward: 0.762
- Average correctness: 0.768

In this simulation, the Q-learning tutor performs better than the random policy.

This suggests that the tutor can learn better decisions inside the simplified environment.

## 7. Key Interpretation

The project successfully connects multiple AI/ML components into one working pipeline.

The main result is not only one model score.

The main result is the complete system:

data → features → supervised prediction → clustering → recommendation → reinforcement learning → evaluation → visualization → demo

## 8. Limitations of Results

The current results should be interpreted carefully.

Important limitations:

- the dataset is synthetic
- student behavior is simulated
- the reinforcement learning environment is simplified
- recommendations are baseline strategies
- no real classroom feedback is used
- no real long-term learning gain is measured

Because of this, the results show that the pipeline works, but they do not prove real-world educational effectiveness yet.

## 9. Next Research Step

The next major research step is to test the pipeline on a real educational dataset.

Possible datasets:

- ASSISTments
- EdNet

Using real data would make the project stronger and more research-ready.

## 10. Summary

The current prototype is successful as a reproducible AI/ML research portfolio project.

It includes:

- working pipeline
- automated test
- supervised learning results
- clustering analysis
- recommendation examples
- reinforcement learning comparison
- visual result outputs
- Streamlit demo
- documentation