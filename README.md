
# M-Motors - Plateforme de Vente et Location de Véhicules

## Description
M-Motors est une application web qui permet aux utilisateurs de vendre, acheter et louer des véhicules. Elle offre une interface intuitive pour gérer les annonces de véhicules et prend en charge les images.

## État actuel du projet
⚠️ **Note importante**: Cette version du projet fonctionne uniquement en local.

### Fonctionnalités disponibles
- Création de compte et authentification.
- Ajout, modification et suppression d'annonces de véhicules.
- Upload et affichage d'images en local.
- Recherche et filtrage des véhicules.
- Gestion de profil utilisateur.

### Limitations connues
- Les images sont stockées localement (pas de stockage cloud).
- Pas de déploiement en production.
- Chatbot non intégré.

## Installation et configuration

### Prérequis
- Python 3.x
- Node.js
- PostgreSQL
- Redis (optionnel, pour la gestion des sessions en production)

### Backend (Flask)
1. Cloner le repository.
2. Créer un environnement virtuel :
   \```bash
   python -m venv .venv
   source .venv/bin/activate # Sur Unix
   .venv\Scripts\activate # Sur Windows
   \```
3. Installer les dépendances :
   \```bash
   cd back-end
   pip install -r requirements.txt
   \```
4. Configurer la base de données dans `.env`.
5. Lancer le serveur :
   \```bash
   python app.py
   \```

### Frontend (React)
1. Installer les dépendances :
   \```bash
   cd front-end
   npm install
   \```
2. Lancer l'application :
   \```bash
   npm run dev
   \```

## Utilisation
1. Créer un compte utilisateur.
2. Se connecter.
3. Pour ajouter un véhicule, cliquer sur "Vendre", remplir les informations du véhicule et ajouter jusqu'à 5 photos. Les photos seront stockées localement dans `back-end/static/uploads/` et visibles dans les annonces.

## Tentatives de déploiement
Nous avons tenté de déployer l'application avec :
- AWS Lightsail pour le backend.
- AWS Amplify pour le frontend.
Nous avons tenté d'utiliser :
- AWS S3 pour le stockage des images.

### Problèmes rencontrés
- Problèmes de configuration avec Lightsail.
- Problèmes de configuration avec Amplify.
- Accès IAM limités pour S3 ce qui nous empêche de stocker les images sur AWS et de s'y connecter.

## Fonctionnalités prévues mais non implémentées
- Intégration d'un chatbot avec Ollama(problème de configuration IAM).
- Stockage des images sur AWS S3(problème de configuration IAM).
- Déploiement complet sur AWS.

## Configuration requise

### Backend (.env)
\```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=votre_clé_secrète
PG_HOST=localhost
PG_PORT=5432
PG_DB=groupe4
PG_USER=postgres
PG_PASSWORD=
\```

### Frontend (config.js)
\```javascript
export const API_URL = 'http://localhost:8000/api';
\```