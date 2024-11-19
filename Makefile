install:
	pipenv install

pytest:
	export ENV=test && pipenv run pytest -v -s -k "order"

dev:
	pipenv run uvicorn src.main:app --reload

dev-con:
	pipenv run uvicorn src.main:app  --host 0.0.0.0 --port 8000
	
serve:
	pipenv run python src/main.py
