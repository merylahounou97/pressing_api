# 🧺 Pressing API

## 🚀 Aperçu du projet
**Pressing API** est une application backend développée avec **FastAPI** pour la gestion complète d’un service de pressing.  
Elle centralise la gestion des **utilisateurs** (clients, secrétaires, administrateurs), le **catalogue d’articles**, les **commandes** et la **facturation** avec envoi automatique par email et SMS.  

L’objectif est de simplifier et d’automatiser les opérations quotidiennes du pressing, depuis la **prise de commande** jusqu’à la **livraison et facturation**.

---

## ✨ Fonctionnalités clés

### 👥 Gestion des utilisateurs
- Trois rôles : **Client**, **Secrétaire**, **Administrateur**  
- Enregistrement, connexion et gestion des profils  
- Création automatique d’un **compte admin par défaut** lors du premier lancement  
- Vérification d’identité via **email** ou **numéro de téléphone** avec code de confirmation (email + SMS)  
- Réinitialisation de mot de passe par **lien sécurisé** envoyé au client  

### 📦 Catalogue d’articles
- Gestion des articles du pressing (type de vêtement, prix, etc.)  
- CRUD complet (ajout, édition, suppression, recherche)  
- Recherche par **nom** ou **code article**  

### 📜 Commandes
- Création, modification, annulation et suivi des commandes  
- Statuts : **En attente**, **En cours**, **Finalisée**, **Annulée**  

### 🧾 Facturation
- Génération de factures **HTML/PDF** basées sur les commandes  
- Respect du format standard du pressing (similaire au fichier Excel de référence)  
- Envoi automatique par **email** au client  
- Sauvegarde des factures au format PDF  

### 📧 Notifications
- Emails : confirmation d’inscription, facture, reset mot de passe  
- SMS (Twilio) : validation de compte, confirmation de téléphone, notifications importantes  

### 🔑 Sécurité
- Hashage des mots de passe avec **bcrypt**  
- Authentification via **JWT Tokens**  
- Vérification d’identité renforcée (email + SMS)  

### ⚙️ Déploiement & CI/CD
- **GitHub Actions** pour CI/CD et déploiement automatisé  
- Hébergement sur **VPS Dockerisé** avec **Traefik** (reverse proxy + HTTPS)  

---

## 🛠️ Stack technique

- **FastAPI** – Framework backend Python  
- **PostgreSQL** – Base de données relationnelle  
- **SQLAlchemy** – ORM pour la gestion des modèles  
- **Alembic** – Migration de schéma  
- **Docker & Docker Compose** – Conteneurisation et orchestration  
- **Traefik** – Reverse proxy & SSL  
- **Jinja2 + WeasyPrint** – Génération de factures HTML/PDF  
- **Twilio** – Envoi de SMS  
- **GitHub Actions** – Intégration & déploiement continu  

---

## 📂 Structure du projet

```
src/
│── auth/             # Authentification & sécurité
│── users/            # Gestion des utilisateurs (clients, secrétaires, admins)
│── customer/         # Gestion des clients
│── catalog/          # Gestion des articles
│── order/            # Gestion des commandes
│── invoice/          # Génération et envoi des factures
│── mail/             # Service email (envoi, templates)
│── sms/              # Service SMS (Twilio, templates)
│── dependencies/     # DB, config, injections de dépendances
│── utils/            # Fonctions utilitaires, constantes
│── lifespans/        # Initialisation (création admin par défaut, setup app)
│── database.py       # Connexion à la base de données
│── config.py         # Paramètres globaux de l'application
│── main.py           # Point d'entrée FastAPI
│── ...
tests/                # Tests unitaires et d’intégration

```

---

## ▶️ Installation & Lancement
### Prérequis
Assurez-vous d'avoir installé Docker et Docker Compose sur votre machine.

### 1. Cloner le projet
```bash
git clone https://github.com/votre-repo/pressing-api.git
cd pressing-api

docker-compose up --build
