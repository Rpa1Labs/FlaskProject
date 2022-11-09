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

Enfin, il faut installer les dépendances du projet :

```bash
cd FlaskProject
pip3 install -r requirements.txt
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

## Utilisation

Si vous lancez le projet sur votre ordinateur, vous pouvez vous rendre sur l'adresse suivante : [http://localhost:5000](http://localhost:5000)

Sinon, vous pouvez vous rendre sur l'adresse suivante : [http://IP_DE_VOTRE_SERVEUR:5000](http://IP_DE_VOTRE_SERVEUR:5000)