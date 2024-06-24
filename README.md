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

# Norme de commit 
feat: Une nouvelle fonctionnalité pour l'utilisateur.
Exemple: feat: ajouter la possibilité de filtrer les résultats de recherche

fix: Une correction de bug.
Exemple: fix: corriger l'affichage incorrect des dates sur le tableau de bord

docs: Des modifications uniquement au niveau de la documentation.
Exemple: docs: mettre à jour le fichier README pour expliquer la nouvelle API

style: Des changements qui n'affectent pas le sens du code (indentation, espaces, formatage, points-virgules manquants, etc.).
Exemple: style: reformater le code selon les nouvelles règles ESLint

refactor: Une modification de code qui n'ajoute pas de fonctionnalité ni ne corrige de bug.
Exemple: refactor: réorganiser les modules pour une meilleure lisibilité

perf: Un changement qui améliore les performances.
Exemple: perf: optimiser la requête SQL pour réduire le temps de réponse

test: Ajout de tests manquants ou correction de tests existants.
Exemple: test: ajouter des tests unitaires pour la fonction de validation des emails

chore: Mise à jour des tâches de build, des outils de génération, des dépendances, etc.
Exemple: chore: mettre à jour les dépendances npm

build: Modifications affectant le système de build ou les dépendances externes (par exemple, gulp, webpack, npm).
Exemple: build: configurer Babel pour la compilation ES6

ci: Modifications aux fichiers et scripts de configuration CI (par exemple, CircleCI, SauceLabs).
Exemple: ci: ajouter la configuration Travis pour les tests automatiques

revert: Revenir à un commit précédent.
Exemple: revert: revenir au commit 12345abcd pour corriger une régression