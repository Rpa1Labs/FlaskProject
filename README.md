# FlaskProject

Petit projet Flask pour tester les fonctionnalités de Flask. Il s'agit d'un site de gestion de livres.

## Installation

Pour installer le projet, il faut d'abord installer les dépendances du projet. Pour cela, il faut se placer dans le dossier du projet et lancer la commande suivante :

Sous debian :

```bash
sudo apt install python3-pip git
```

Sous fedora :

```bash
sudo dnf install python3-pip git
```

Ensuite, il faut cloner le projet :

```bash
git clone https://github.com/Rpa1Labs/FlaskProject
```

Il faut installer les dépendances du projet :

```bash
cd FlaskProject
pip3 install -r requirements.txt
```

Il faut créer la base de données :

```bash
python3 -m flask syncdb
```

Enfin, il faut créer un utilisateur :

```bash
python3 -m flask newuser <username> <password>
``` 

## Lancement

Pour lancer le projet, il faut se placer dans le dossier du projet et lancer la commande suivante :

```bash
python3 -m flask run
```

Si vous souhaitez que le projet soit accessible depuis un autre ordinateur, il faut lancer la commande suivante :

```bash
python3 -m flask run --host 0.0.0.0
```

Vous pouvez ajouter des livres sous le format suivant :

```yaml
- author: Auteur
  img: nom_de_l_image.jpg
  price: 10.00
  title: Titre
  url: https://url_du_livre.com
```

Pour les ajouter, il faut dans un premier temps mettre les images dans le dossier `static/images` et ensuite éxécuter la commande suivante :

```bash
python3 -m flask loaddb <fichier yaml>
```


## Utilisation

Si vous lancez le projet sur votre ordinateur, vous pouvez vous rendre sur l'adresse suivante : [http://localhost:5000](http://localhost:5000)

Sinon, vous pouvez vous rendre sur l'adresse suivante : [http://IP_DE_VOTRE_SERVEUR:5000](http://IP_DE_VOTRE_SERVEUR:5000)