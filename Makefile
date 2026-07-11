.PHONY: install pipeline test demo check clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

pipeline:
	python run_pipeline.py

test:
	pytest

demo:
	streamlit run 07_demo/app.py

check:
	python run_pipeline.py
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -delete