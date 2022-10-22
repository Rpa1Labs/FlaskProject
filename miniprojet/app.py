from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



def mkpath(p):
    """
    Renvoie le chemin complet du répertoire p passé en paramètre
    """
    return os.path.join(os.path.dirname(__file__), p)


# Création de l'application Flask
app = Flask(__name__)

# Configuration de l'application Flask
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + mkpath('../books.db')
app.config['SECRET_KEY'] = 'e56a297a-70cc-465a-a6bc-a4dc575ab4a2'

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Initialisation de l'extension Bootstrap 5
bootstrap = Bootstrap5(app)

# Initialisation de l'extension Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"