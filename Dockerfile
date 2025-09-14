FROM python:3.10

EXPOSE 8000

WORKDIR /app

RUN python -m pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

CMD ["fastapi", "run", "src/main.py", "--proxy-headers", "--port", "8000", "--root-path","/pressing_api"]