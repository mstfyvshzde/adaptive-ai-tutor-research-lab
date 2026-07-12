# EdNet External Dataset

This folder is reserved for EdNet real educational interaction data.

## Important Note

Raw EdNet files should not be committed to GitHub.

Large raw dataset files must stay local because they can be too large for the repository and may have dataset usage restrictions.

## Dataset Role in This Project

EdNet will be used in V2 to validate the adaptive AI tutor pipeline on real educational interaction data.

The planned subset will focus on question-answer interactions and correctness prediction.

## Planned Subset

Target subset:

- Around 10,000 students
- Around 500,000 interactions
- Minimum 20 interactions per student
- Question-answer interactions only
- Correctness prediction task

## Expected Columns After Mapping

The raw EdNet data will be mapped into the project format:

- student_id
- question_id
- timestamp
- tags or skill
- elapsed_time
- is_correct

## Why a Subset?

The full EdNet dataset is very large. A controlled subset keeps the experiment reproducible, manageable, and focused on the research goal.

The goal of V2 is real-data validation, not full-scale EdNet processing.