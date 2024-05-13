# pressing_api
Cette api est une api pour gérer le pressing de Méryl

# Pour démarer le projet

## En local

- Cloner le projet
- exécuter la commande `pip install pipenv` pour instaler pipenv
- exécuter `pipenv install` pour installer toutes les dépendances du projet
- exécuter `make dev` pour démarer le projet en mode développement

## Avec docker
Exécuter la commande ci-dessous pour lancer le projet en mode container

`docker compose up` 
ou
 `docker compose watch` 
 pour le lancer en mode container developpement

# Lancer les tests
Pour lancer les test il faut exécuter la commande `make test`

# Chargement des fichiers statics
Pour charger les fichiers statiques comme les images et autres, 
en local il faut changer la valeur de la variable d'environnement api_url.
A cet effet on peut utiliser [](ngrok)
Notamment il faut exécuter `ngrok http 8000` 