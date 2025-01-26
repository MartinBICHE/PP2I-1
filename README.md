# CodeSafe

## Abstract
Dans le cadre de notre **Projet Pluridisciplinaire d'Informatique Intégrative**,\
nous avons décidé de créer un site web interactif à visée éducative :\
sensibiliser à la sécurité informatique au travers de quizz, test de mots de passe, etc.

## Réalisation du projet
Par *BICHE Martin, QUILLIOT Ethan, GURTNER Léo & WERCK Hugo.*

## Faire fonctionner le site web

### 1. Cloner ce projet
```bash
git clone https://github.com/nom-du-repo/CodeSafe.git
cd CodeSafe
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv env
```

### 3. Activer l'environnement virtuel
- Sur macOS/Linux :
  ```bash
  source env/bin/activate
  ```
- Sur Windows :
  ```powershell
  .\env\Scripts\activate
  ```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Lancer le fichier `app.py`
```bash
python3 app.py
```

### 6. Désactiver l'environnement virtuel après utilisation
```bash
deactivate
```

## Inscription et connexion

1. Sur la page d'accueil du site, cliquez sur le bouton **"S'inscrire"** en haut à droite.
2. Entrez un **login** et un **mot de passe**.
   - Le mot de passe doit être suffisamment costaud, sinon l'inscription ne sera pas validée.
3. Une fois inscrit, cliquez sur le bouton **"Connexion"**.
4. Renseignez les informations de connexion utilisées lors de l'inscription.
5. Une fois connecté, vous aurez un accès total aux **questionnaires** et aux **statistiques**.

### Utilisateur existant
Un utilisateur par défaut est déjà disponible :
- **Login :** `main`
- **Mot de passe :** `Main123`

Vous pouvez utiliser ces identifiants pour vous connecter directement.

