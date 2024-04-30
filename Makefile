install:
	pipenv install

test:
	pipenv run pytest -vv

cov:
	pipenv run pytest --cov

dev:
	pipenv run uvicorn src.main:app --reload

dev-con:
	uvicorn src.main:app  --host 0.0.0.0 --port 8000
	
serve:
	pipenv run python src/main.py