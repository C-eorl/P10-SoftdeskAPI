# Desksoft API
![logo Desksoft](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

## Création d'une API RESTful sécurisée en utilisant Django REST

---
## I - Installation

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

Utilisez l'url pour acceder à l'API : http://127.0.0.1:8000/

---
_Projet réalisée dans le contexte de la formation Developpeur Python - OpenClassRoom_