# LITRevu
LITRevu est une application permettant de demander ou publier des critiques de livres ou d'articles.
Ce dépôt contient une application web servant à la mise en place d'un produit viable minimum.

Ce travail est issu du projet 9 de la formation DA Python OpenClassrooms.

Il est développé avec [Python 3.11](https://www.python.org/downloads/release/python-3110/) sur Windows 11 Pro.

#### Cloner le projet, installer l'environnement virtuel et l'activer :

Rendez vous dans le dossier de votre choix et cloner le projet avec : \
`git clone https://github.com/Roxhe/litrevu.git`

Rendez vous dans le dossier du projet avec `cd litrevu`, puis installer l'environnement virtuel avec : \
`python -m venv 'env'`  

Puis activez le avec : \
`source env/Scripts/activate`

#### Installer les modules nécessaire dans l'environnement virtuel :

Toujours dans le dossier du projet, exécuter : \
`pip install -r requirements.txt`

Puis rendez-vous dans le dossier de l'application avec `cd litrevu`.

Une fois dans le dossier, exécutez : \
`python manage.py makemigrations` puis `python manage.py migrate` 

Puis lancez le site sur votre serveur local en exécutant la commande : \
`python manage.py runserver`

#### Effectuer les tests sur le site :

Lancez votre navigateur et rendez vous sur l'adresse `http://127.0.0.1:8000`

Vous pouvez soit vous connecter aux deux comptes pré-existant suivant : \
Nom d'utilisateur : `moonlight` Mot de passe : `Moonlight1` \
Nom d'utilisateur : `Sunlight` Mot de passe : `Sunlight1` \

Ou bien créer un compte vierge.

