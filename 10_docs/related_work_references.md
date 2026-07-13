# Related Work and References

## 1. Intelligent Tutoring Systems and Educational Data Mining

Intelligent tutoring systems aim to personalize learning by modeling student knowledge, selecting appropriate learning activities, and providing feedback. In educational data mining, student interaction data is used to understand learning behavior, predict future performance, and support adaptive learning decisions.

This project fits into educational data mining because it uses student interaction history to predict correctness and analyze how performance changes across dataset scale.

## 2. Knowledge Tracing

Knowledge Tracing is the task of modeling a student's evolving knowledge state over time. In practice, many KT systems predict whether a student will answer a future question correctly based on previous responses.

This project does not propose a new KT algorithm. Instead, it builds an applied ML validation pipeline using knowledge tracing-inspired history features.

## 3. Bayesian Knowledge Tracing

Bayesian Knowledge Tracing is one of the classical approaches to modeling student knowledge. It treats mastery as a latent state and updates the probability of mastery based on student responses.

BKT is important because it provides an interpretable foundation for student modeling. However, it usually depends on skill-level assumptions and manually defined knowledge components.

## 4. Deep Knowledge Tracing

Deep Knowledge Tracing introduced recurrent neural networks for modeling student learning sequences. DKT showed that neural sequence models can capture complex temporal patterns in student responses.

This project does not yet implement DKT. However, DKT is a natural future extension because the EdNet KT1 data contains sequential student interaction histories.

## 5. Attention-Based Knowledge Tracing

Attention-based KT methods, such as SAKT and AKT, use attention mechanisms to identify which previous interactions are most relevant to a current prediction.

These models are important future baselines for this project because they can potentially model long student histories more flexibly than classic ML models.

## 6. EdNet Dataset

EdNet is a large-scale hierarchical educational dataset collected from a real AI tutoring platform. It contains student interactions across multiple levels of abstraction and supports tasks such as knowledge tracing and learning path recommendation.

This project uses the KT1 level of EdNet, focusing on question-solving interactions and correctness prediction.

## 7. Position of This Project

This project should be positioned as an applied machine learning research portfolio project rather than a novel algorithm paper.

The main contribution is not a new model architecture. The main contribution is a clean, reproducible, leakage-aware validation pipeline that connects:

- synthetic adaptive tutor prototyping
- real educational data validation
- correctness prediction
- scale experiments
- ablation analysis
- feature importance
- error analysis
- responsible reporting

## 8. Key References

### EdNet

Choi, Y., Lee, Y., Shin, D., Cho, J., Park, S., Lee, S., Baek, J., Bae, C., Kim, B., & Heo, J. (2019).  
**EdNet: A Large-Scale Hierarchical Dataset in Education.**  
arXiv:1912.03072.

### Bayesian Knowledge Tracing

Corbett, A. T., & Anderson, J. R. (1995).  
**Knowledge tracing: Modeling the acquisition of procedural knowledge.**  
User Modeling and User-Adapted Interaction.

### Deep Knowledge Tracing

Piech, C., Spencer, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. (2015).  
**Deep Knowledge Tracing.**  
arXiv:1506.05908.

### Self-Attentive Knowledge Tracing

Pandey, S., & Karypis, G. (2019).  
**A Self-Attentive Model for Knowledge Tracing.**  
arXiv:1907.06837.

### Context-Aware Attentive Knowledge Tracing

Ghosh, A., Heffernan, N., & Lan, A. S. (2020).  
**Context-Aware Attentive Knowledge Tracing.**  
arXiv:2007.12324.

### Knowledge Tracing Survey

Abdelrahman, G., Wang, Q., & Nunes, B. P. (2022).  
**Knowledge Tracing: A Survey.**  
arXiv:2201.06953.

### Additional Knowledge Tracing Survey

Shen, S., Liu, Q., Huang, Z., Zheng, Y., Yin, M., Wang, M., & Chen, E. (2021).  
**A Survey of Knowledge Tracing: Models, Variants, and Applications.**  
arXiv:2105.15106.

### DKT Interpretation Discussion

Khajah, M., Lindsey, R. V., & Mozer, M. C. (2016).  
**How Deep Is Knowledge Tracing?**  
arXiv:1604.02416.
