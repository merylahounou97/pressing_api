FROM python:3.10

EXPOSE 8000

WORKDIR /app

RUN pip install pipenv 

COPY Pipfile Pipfile.lock ./

RUN pipenv install 

COPY . .



CMD  ["make","dev-con"]