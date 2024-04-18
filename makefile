install:
	pipenv install

test:
	pipenv run pytest

lint:
	pipenv run flake8 src

dev:
	uvicorn src.main:app --reload
	
serve:
	pipenv run python src/main.py
