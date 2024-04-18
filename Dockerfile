# Utiliser une image de base officielle Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN pip install pipenv 

COPY Pipfile Pipfile.lock ./

RUN pipenv  install --deploy --system

COPY ./src ./src

# Exposer le port sur lequel FastAPI sera accessible
EXPOSE 8000

# Commande pour lancer l'application en utilisant uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
