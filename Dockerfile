FROM python:3.10

EXPOSE 8000

WORKDIR /app

RUN python -m pip install --upgrade pip && pip install --user pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]