# Deployment Notes

## 1. Overview

This document explains possible deployment options for the Adaptive AI Tutor Research Lab.

The current project is a research prototype with a local Streamlit demo.

The main demo command is:

`streamlit run 07_demo/app.py`

## 2. Current Deployment Status

Current status:

- local pipeline works
- automated test passes
- Streamlit demo runs locally
- GitHub Actions CI is planned
- production deployment is not included yet

This is enough for a portfolio prototype.

## 3. Local Demo

To run the project locally:

`python run_pipeline.py`

Then launch the demo:

`streamlit run 07_demo/app.py`

The demo reads generated CSV and PNG files from the results folders.

## 4. Possible Deployment Options

Future deployment options include:

- Streamlit Community Cloud
- Hugging Face Spaces
- Docker container
- FastAPI backend with separate frontend
- cloud deployment on services such as Render, Railway, or AWS

## 5. Streamlit Cloud Option

Streamlit Community Cloud is a simple option for sharing the demo.

Possible steps:

1. Push the project to GitHub.
2. Connect the repository to Streamlit Cloud.
3. Select `07_demo/app.py` as the app entry point.
4. Make sure dependencies are listed in `requirements.txt`.
5. Run the pipeline before deployment or include demo-ready output files if appropriate.

## 6. Hugging Face Spaces Option

Hugging Face Spaces can also host Streamlit apps.

Possible steps:

1. Create a new Space.
2. Choose Streamlit as the SDK.
3. Upload or connect the project files.
4. Include `requirements.txt`.
5. Make sure the demo can access required result files.

## 7. Docker Option

A future Docker setup could make the project easier to run in a consistent environment.

A Docker-based version could:

- install dependencies
- run the pipeline
- launch the Streamlit demo
- make deployment more reproducible

## 8. Production Backend Option

If this project becomes a real product, the Streamlit demo would not be enough.

A stronger architecture could include:

- FastAPI backend
- database
- model service
- user authentication
- monitoring system
- frontend learning interface

## 9. Current Limitation

The current demo depends on generated local result files.

Because of this, deployment should make sure that required CSV and PNG outputs are available.

The safest current workflow is:

`python run_pipeline.py`

then

`streamlit run 07_demo/app.py`

## 10. Summary

The current project is ready as a local portfolio demo.

Future deployment can use Streamlit Cloud, Hugging Face Spaces, Docker, or a full backend architecture depending on the project direction.