install:
	pipenv install

pytest:
	PIPENV_DONT_LOAD_ENV=1 ENV=test DATABASE_NAME=test pipenv run pytest -v -s 

dev:
	pipenv run uvicorn src.main:app --reload

dev-con:
	pipenv run uvicorn src.main:app  --host 0.0.0.0 --port 8000
	
serve:
	pipenv run python src/main.py
