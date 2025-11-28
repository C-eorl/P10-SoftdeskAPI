# Desksoft API
![logo Desksoft](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

## Index

- [Introduction](#introduction)
- [Structure](#structure)
- [Installation](#installation)
- [Documentation](#documentation)

## Introduction
**Création d'une API RESTful sécurisée en utilisant Django REST**
Cette API REST permet de gérer des projets, contributeurs, issues et commentaires, 
avec une architecture robuste basée
sur Django REST Framework, JWT Authentication et des routes imbriquées via drf-nested-routers.

## Structure
```commandline
Softdesk/
├── authentication/         #
│   ├── models.py           #   Module d'authentification
│   ├── serializers.py      #   utilisant JWT
│   ├── urls.py             #
│   └── views.py            #
|
├── tracking_projects/      #         
│   ├── models.py           #
│   ├── permissions.py      #   Module 
│   ├── serializers.py      #   Project, Contributor,
│   ├── urls.py             #   Issue, Comment
│   └── views.py            #
|
├── config/                 #   Module configuration DRF
|
├── pyproject.toml          #
├── README.MD               #   fichier d'information & configuration
├── requirements.txt        #
├── uv.lock                 #
|
├── manage.py               
└── db.sqlite3              


```

---
## Installation

### 1. Cloner le dépôt
```bash
  git clone git@github.com:C-eorl/P10-SoftdeskAPI.git 
  cd P10-SoftdeskAPI
```
### 2. Installer l'environnement virtuel

#### a. Via pip  
* Création & activation de l'environnement 
```bash
    python -m venv venv
    source venv/bin/activate   # sous Windows : venv\Scripts\activate
```
* Installation des dépendances
```bash
    pip install -r requirements.txt
```

#### b. Via UV 
```bash
    uv install
```

### 3. Démarrer le serveur
```bash
    python manage.py runserver
    # ou si utilisation UV
    uv run manage.py runserver
```

### 4. Acceder à l'API

Utilisez l'url pour acceder à l'API : `http://127.0.0.1:8000/api/v1/`

---
## Documentation

**Schema d'url:** `base_url`/`endpoint`

### - Endpoints

#### Authentification

* Création d'un compte utilisateur
    - POST `/auth/register/`
* Accès au profil de l'utilisateur
    - GET `/auth/profile/`
* Modification du compte utilisateur
  - PUT ou PATCH `/auth/profile/`
* Suppression du compte utilisateur
  - DELETE `/auth/profile/`
---
#### JWT
* Obtention token jwt
  - POST `/token/`
* Rafraichissement token jwt
  - POST `/token/refresh/`
---
#### Projects
* Liste des projets (filtrage si contributeur du projet)
  - GET `/projects/`
* Détails d'un projet 
  - GET `/projects/<project_id>/`
* Création d'un projet 
  - POST `/projects/`
* Modification d'un projet 
  - PATCH `/projects/<project_id>/`
* Suppression d'un projet 
  - DELETE `/projects/<project_id>/`
---
#### Contributors
* Liste des contributeurs 
  - GET `/projects/<project_id>/contributors/`
* Détails d'un contributeur 
  - GET `/projects/<project_id>/contributors/<contributor_id>/`
* Création d'un contributeur 
  - POST `/projects/<project_id>/contributors/`
* Suppression d'un contributeur 
  - DELETE `/projects/<project_id>/contributors/<contributor_id>/`
---
#### Issues
* Liste des problèmes / taches 
  - GET `/projects/<project_id>/issues/`
* Détails d'un problème / tache 
  - GET `/projects/<project_id>/issues/<issue_id>/`
* Création d'un problème / tache 
  - POST `/projects/<project_id>/issues/`
* Modification d'un problème / tache
    - PATCH `/projects/<project_id>/issues/<issue_id>/`
* Suppression d'un problème / tache 
  - DELETE `/projects/<project_id>/issues/<issue_id>/`
---
#### Comments
* Liste des commentaires 
  - GET `/projects/<project_id>/issues/<issue_id>/comments/`
* Détails d'un commentaire (problème/tache) 
  - GET `/projects/<project_id>/issues/<issue_id>/comments/<comment_uuid>/`
* Création d'un commentaire (problème/tache) 
  - POST `/projects/<project_id>/issues/<issue_id>/comments/`
* Modification d'un commentaire (problème/tache)
    - PATCH `/projects/<project_id>/issues/<issue_id>/<comment_uuid>/`
* Suppression d'un commentaire (problème/tache) 
  - DELETE `/projects/<project_id>/issues/<issue_id>/<comment_uuid>/`

---
### - Permissions
Permissions utilisées:
- `IsAuthenticated`  $${\color{yellow}■}$$
- `IsContributor` $${\color{cyan}■}$$
- `IsAuthor` $${\color{red}■}$$   

| Ressource       | Lire                         | Créer                            | Modifier / Supprimer           |
|-----------------|------------------------------|----------------------------------|--------------------------------|
| **Project**     | $\color{cyan}is-contributor$ | $\color{yellow}is-authenticated$ | $\color{red}is-author-project$ |
| **Contributor** | $\color{cyan}is-contributor$ | $\color{red}is-author-project$   | $\color{red}is-author-project$ |
| **Issue**       | $\color{cyan}is-contributor$ | $\color{cyan}is-contributor$     | $\color{red}is-author-issue$   |
| **Comment**     | $\color{cyan}is-contributor$ | $\color{cyan}is-contributor$     | $\color{red}is-author-comment$ |

---
_Projet réalisée dans le contexte de la formation Developpeur Python - OpenClassRoom_