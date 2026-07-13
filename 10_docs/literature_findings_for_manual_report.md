# Literature Findings for Manual Final Report

This file contains citation-ready notes for the manually written final report.

## Recommended Citation Style

Use simple in-text citations:

- (Choi et al., 2019)
- (Corbett & Anderson, 1995)
- (Piech et al., 2015)
- (Pandey & Karypis, 2019)
- (Ghosh et al., 2020)
- (Abdelrahman et al., 2022)
- (Shen et al., 2021)

## EdNet

EdNet is a large-scale hierarchical educational dataset introduced by Choi et al. (2019). The dataset contains 131,441,538 interactions from 784,309 students collected over more than two years. It was designed to support tasks such as knowledge tracing and learning path recommendation.

Suggested sentence for report:

> EdNet is an appropriate real-data benchmark for this project because it contains large-scale student interaction data and supports tasks such as knowledge tracing and learning path recommendation (Choi et al., 2019).

## Bayesian Knowledge Tracing

Bayesian Knowledge Tracing is a classical student modeling approach that estimates a learner's hidden mastery state and updates this estimate after observed responses (Corbett & Anderson, 1995). Its main strength is interpretability, but it usually depends on predefined knowledge components and simplifying assumptions about learning.

Suggested sentence for report:

> Bayesian Knowledge Tracing provides an interpretable foundation for student modeling, but it relies on assumptions about hidden mastery states and predefined knowledge components (Corbett & Anderson, 1995).

## Deep Knowledge Tracing

Deep Knowledge Tracing introduced recurrent neural networks for modeling student learning sequences (Piech et al., 2015). The paper argued that RNN-based models can capture complex representations of student knowledge without explicitly encoding human domain knowledge.

Suggested sentence for report:

> Deep Knowledge Tracing showed that recurrent neural networks can model student response sequences without manually encoding domain-specific knowledge structures (Piech et al., 2015).

## Self-Attentive Knowledge Tracing

SAKT uses self-attention to identify relevant past interactions for a current prediction (Pandey & Karypis, 2019). The authors report that SAKT outperformed prior knowledge tracing models and improved AUC by 4.43% on average across several real-world datasets.

Suggested sentence for report:

> Self-Attentive Knowledge Tracing uses self-attention to select relevant previous interactions and was reported to improve AUC by 4.43% on average across several real-world datasets (Pandey & Karypis, 2019).

## Context-Aware Attentive Knowledge Tracing

AKT combines attention-based neural modeling with interpretable components inspired by cognitive and psychometric models (Ghosh et al., 2020). The authors report improvements of up to 6% AUC in some benchmark settings.

Suggested sentence for report:

> Context-Aware Attentive Knowledge Tracing combines attention mechanisms with interpretable cognitive and psychometric components, achieving up to 6% AUC improvement in some benchmark settings (Ghosh et al., 2020).

## Knowledge Tracing Surveys

Recent surveys organize the knowledge tracing field into classical, deep learning, memory-based, attention-based, and graph-based approaches (Abdelrahman et al., 2022; Shen et al., 2021). These surveys are useful for positioning this project as an applied classical ML baseline rather than a novel deep KT architecture.

Suggested sentence for report:

> Recent knowledge tracing surveys show that the field has moved from classical probabilistic models toward deep, attention-based, and graph-based models, which frames this project as a classical ML baseline rather than a frontier KT architecture (Abdelrahman et al., 2022; Shen et al., 2021).

## Positioning Statement

Use this wording in the manual report:

> This project is positioned as a reproducible applied machine learning portfolio project for educational data mining. It does not propose a new knowledge tracing architecture; instead, it evaluates leakage-aware classical ML baselines on a real EdNet KT1 subset and reports scale behavior, feature importance, and error patterns.

## What Not to Claim

Do not claim:

- Harvard-level academic research.
- State-of-the-art knowledge tracing.
- Novel algorithmic contribution.
- Full EdNet benchmark comparison.
- Production-ready adaptive tutor.

Safe claim:

> Strong applied ML research portfolio project.
