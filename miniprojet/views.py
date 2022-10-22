###########
# Imports #
###########




from .app import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators, PasswordField, SelectField, FloatField, URLField
from hashlib import sha256
from flask_wtf.file import FileField, FileAllowed
import os

from .models import get_sample, get_user_by_mail, get_users, load_user, get_book_details, get_books_by_author, get_authors, get_author
from .models import Author, User, Book


















###############
# Formulaires #
###############

# Réponse à la vie, l'univers et tout le reste sur cette ligne


class AuthorForm(FlaskForm):
    """
    Classe du formulaire d'ajout d'un auteur avec les champs suivants:
    - id: champ caché
    - name: nom de l'auteur (champ obligatoire)
    """

    id = HiddenField('id')

    name = StringField('Nom', [
        validators.InputRequired(),
        validators.Length(
            min=2,
            max=25,
            message="Le nom doit faire entre 2 et 25 caractères"),
        validators.Regexp(
            r'^[a-zA-Z \.\-]+$',
            message=
            "Le nom ne doit contenir que des lettres, des espaces, des points et des tirets"
        )
    ])



# Noice ! 69, mon nombre préféré !



class BookForm(FlaskForm):
    """
    Classe du formulaire d'ajout d'un livre avec les champs suivants:
    - id: champ caché
    - title: titre du livre (champ obligatoire)
    - author_id: id de l'auteur (champ obligatoire)
    - price: prix du livre (champ obligatoire)
    - img: image de couverture du livre (champ optionnel)
    - url: url du livre (champ obligatoire)
    """

    id = HiddenField('id')

    title = StringField('Titre', [
        validators.InputRequired(),
        validators.Length(
            min=2,
            max=45,
            message="Le titre doit faire entre 2 et 50 caractères")
    ])

    author_id = SelectField('Auteur',
                            coerce=int,
                            validators=[validators.InputRequired()],
                            choices=[],
                            validate_choice=False)

    price = FloatField('Prix', [validators.InputRequired()])

    url = URLField('URL', [validators.InputRequired()])

    img = FileField(
        'Image', validators=[FileAllowed(['jpg', 'png'], 'Images uniquement')])

    def validate_author_id(self, author_id):
        if not get_author(author_id.data):
            raise validators.ValidationError("L'auteur n'existe pas")






class LoginForm(FlaskForm):
    """
    Classe du formulaire de connexion avec les champs suivants:
    - username: nom d'utilisateur (champ obligatoire)
    - password: mot de passe de l'utilisateur (champ obligatoire)
    """
    username = StringField('Nom d\'utilisateur')
    password = PasswordField('Mot de passe')

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        print(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode('utf-8'))

        passwd = m.hexdigest()
        return user if passwd == user.password else None


class AdminForm(FlaskForm):
    """
    Classe du formulaire d'ajout d'un utilisateur avec les champs suivants:
    - username: nom d'utilisateur (champ obligatoire)
    - password: mot de passe de l'utilisateur (champ obligatoire)
    - email: email de l'utilisateur (champ obligatoire)
    """
    username = StringField('username', [validators.InputRequired(), validators.Length(min=2, max=50), validators.Regexp(r'^[a-zA-Z0-9_]+$')])
    password = PasswordField('Password', [ validators.Length(min=0, max=50, message="Le mot de passe doit faire au plus 50 caractères")])
    email = StringField('Email', [validators.InputRequired()])





















##########
# Routes #
##########


@app.route("/logout/")
@login_required
def logout():
    """
    Fonction de déconnexion
    """

    #On déconnecte l'utilisateur
    logout_user()

    #On redirige vers la page d'accueil
    return redirect(url_for('home'))




@app.route("/login/", methods=(
    "GET",
    "POST",
))
def login():
    """
    Fonction de connexion
    """

    #Récupération du formulaire
    f = LoginForm()

    #Si le formulaire est validé
    if f.validate_on_submit():

        #On vérifie si le nom d'utilisateur et le mot de passe sont corrects
        user = f.get_authenticated_user()
        if user:
            #Si oui, on connecte l'utilisateur et on le redirige vers la page d'accueil
            login_user(user)
            return redirect(url_for("home"))
        else:
            #Sinon, on affiche un message d'erreur sur le formulaire de connexion
            f.username.errors += ("Nom d'utilisateur ou mot de passe incorrect",)
    return render_template("loginBS.html", form=f)




@app.route("/edit/author")
@app.route("/edit/author/")
@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id=None):
    """
    Fonction d'édition d'un auteur
    """
    
    nom = None

    #Si l'id est renseigné, on récupère l'auteur correspondant
    if id is not None:
        a = get_author(id)
        nom = a.name
    else:
        a = None

    #Création du formulaire avec les données de l'auteur (si il existe)
    f = AuthorForm(id=id, name=nom)

    #On retourne le template d'édition d'auteur avec le formulaire
    return render_template("edit-authorBS.html", author=a, form=f)




@app.route("/save/author/", methods=("POST", ))
@login_required
def save_author():
    """
    Fonction pour créer ou modifier un auteur
    """

    #Récupération du formulaire
    f = AuthorForm()

    #Si l'id est renseigné, on récupère l'auteur correspondant (sinon, on crée un nouvel auteur)
    if f.id.data != "":
        id = int(f.id.data)
        a = get_author(id)
    else:
        a = Author(name=f.name.data)
        db.session.add(a)

    #On met à jour les données de l'auteur
    if f.validate_on_submit():
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('author', id=a.id))

    return render_template("edit-authorBS.html", author=a, form=f)




@app.route("/remove/author/<int:id>")
@login_required
def remove_author(id):
    """
    Fonction pour supprimer un auteur
    """

    #On récupère les livres de l'auteur
    bs = get_books_by_author(id)

    #Si l'auteur a des livres, on supprime les livres
    for b in bs:

        #Si le livre a une image, on la supprime
        if b.img:
            os.remove(os.path.join(app.static_folder + '/images/', b.img))
            
        #On supprime le livre de la base de données
        db.session.delete(b)
    
    #On applique les changements sur la base de données
    db.session.commit()

    #On récupère l'auteur
    a = get_author(id)

    #On supprime l'auteur de la base de données
    db.session.delete(a)

    #On applique les changements sur la base de données
    db.session.commit()

    #On redirige vers la page des auteurs
    return redirect(url_for('authors'))




@app.route("/edit/book")
@app.route("/edit/book/")
@app.route("/edit/book/<int:id>")
@login_required
def edit_book(id=None):
    """
    Fonction d'édition d'un livre
    """
    title = None
    author = None

    #Si l'id est renseigné, on récupère le livre correspondant, sinon on crée un nouveau livre
    if id is not None:
        b = get_book_details(id)
        title = b.title
        author = b.author_id
        price = b.price
        url = b.url
    else:
        b = None
        title = ""
        author = request.args.get('a', default=-1, type=int)
        price = 0
        url = ""

    #Création du formulaire avec les données du livre (si il existe)
    f = BookForm(id=id, title=title, author_id=author, price=price, url=url)
    
    #Création de la liste des auteurs
    f.author_id.choices = [(-1, "Choisissez un auteur")] + [(int(a.id), a.name) for a in get_authors()]
    f.author_id.default = author

    #On retourne le template d'édition de livre avec le formulaire
    return render_template("edit-bookBS.html", book=b, form=f)




@app.route("/save/book/", methods=("POST", ))
@login_required
def save_book():
    """
    Fonction pour créer ou modifier un livre
    """

    #On récupère le formulaire, si l'id n'est pas renseigné, on crée le livre
    f = BookForm()
    if f.id.data != "":
        id = int(f.id.data)
        b = get_book_details(id)
    else:
        b = Book(title=f.title.data,
                 author_id=f.author_id.data,
                 price=f.price.data,
                 url=f.url.data)
        db.session.add(b)

    #Si le formulaire est valide
    if f.validate_on_submit():

        #Recupère les infos du formulaire
        b.title = f.title.data
        b.author_id = f.author_id.data
        b.price = f.price.data
        b.url = f.url.data

        #Si une image est fournie
        if f.img.data:
            #Si le livre avait déjà une image (dans la db), on la supprime
            if b.img:
                try:
                    os.remove(os.path.join(app.static_folder + '/images/', b.img))
                except:
                    pass

            #On ajoute le nouveau nom de l'image dans la db
            b.img = f.img.data.filename

            #On regarde si le nom de l'image respecte les standards, sinon on le modifie
            forbidden_chars = '"*\\/\'.|?:<>'
            b.img = ''.join([x if x not in forbidden_chars else '#' for x in  b.img])
            if len(b.img) >= 166:
                b.img = b.img[:160]

            #Si une image avec le même nom existe déjà, on change le nom de la nouvelle image en ajoutant un nombre au début
            if os.path.exists(os.path.join(app.static_folder + '/images/', f.img.data.filename)):
                i = 1
                while os.path.exists(os.path.join(app.static_folder + '/images/', str(i) + f.img.data.filename)):
                    i += 1
                b.img = str(i) + f.img.data.filename

            #On sauvegarde l'image dans le dossier static/images
            f.img.data.save(os.path.join(app.static_folder + '/images/', b.img))

        #On sauvegarde les modifications dans la db
        db.session.commit()

        #On redirige vers la page du livre
        return redirect(url_for('details', id=b.id))

    #Si le formulaire n'est pas valide, on réaffiche la page d'édition
    f.author_id.choices = [(-1, "Choisissez un auteur")
                           ] + [(int(a.id), a.name) for a in get_authors()]
    f.author_id.default = b.author_id
    return render_template("edit-bookBS.html", book=b, form=f)




@app.route("/remove/book/<int:id>")
@login_required
def remove_book(id):
    """
    Fonction pour supprimer un livre
    """
    #On récupère le livre dans la db
    b = get_book_details(id)

    #Si le livre n'existe pas, on renvoie une erreur 404
    if b is None:
        abort(404)

    #Si le livre a une image, on la supprime
    if b.img:
        os.remove(os.path.join(app.static_folder + '/images/', b.img))

    #On supprime le livre de la db
    db.session.delete(b)

    #On sauvegarde les modifications dans la db
    db.session.commit()

    #On redirige vers la page d'accueil
    return redirect(url_for('home'))




@app.route("/")
def home():
    """
    Fonction de la page d'accueil qui affiche les livres (12 par page)
    """

    #On récupère la page demandée (par défaut 1)
    page = request.args.get('p', default=1, type=int)

    #On récupère les livres de la page demandée
    books, page, isFirst, isLast = get_sample(int(page))

    #On renvoie la page d'accueil avec les livres
    return render_template("booksBS.html",
                           books=books,
                           page=page,
                           isFirst=isFirst,
                           isLast=isLast)




@app.route("/details/<int:id>")
def details(id):
    """
    Fonction qui affiche les détails d'un livre
    """

    #On récupère le livre dans la db
    book = get_book_details(id)

    #Si le livre n'existe pas, on renvoir une erreur 404
    if book is None:
        abort(404)

    #On renvoie la page de détails du livre
    return render_template("detailsBS.html", book=book)




@app.route("/author/<int:id>")
def author(id):
    """
    Fonction qui affiche les livres d'un auteur
    """

    #On récupère les détails de l'auteur
    author = get_author(id)

    #Si l'auteur n'existe pas, on met une erreur 404
    if author is None:
        abort(404)

    #On récupère les livres de l'auteur
    books = get_books_by_author(id)

    #On renvoie le template avec les livres de l'auteur
    return render_template("authorBS.html", author=author, books=books)




@app.route("/authors")
def authors():
    """
    Fonction qui retourne la liste des auteurs
    """

    #On récupère la liste des auteurs dans la db et on la renvoie dans le template correspondant
    authors = get_authors()
    return render_template("authorsBS.html", authors=authors)




@app.route("/admins")
@login_required
def admins():
    """
    Fonction qui permet d'afficher la liste des administrateurs
    """

    #On récupère la liste des administrateurs dans la db et on la renvoie dans le template correspondant
    admins = get_users()
    return render_template("adminsBS.html", admins=admins)




@app.route("/edit/admin")
@app.route("/edit/admin/")
@app.route("/edit/admin/<username>")
@login_required
def edit_admin(username=None):
    """
    Fonction qui permet de générer le formulaire d'édition d'un utilisateur
    """

    #Si on a un nom d'utilisateur, on récupère les détails de l'utilisateur dans la db, sinon on crée un nouvel utilisateur
    if username is not None:
        u = load_user(username)
        username = u.username
        password = u.password
        mail = u.email
    else:
        u = None
        username = ""
        password = ""
        mail = ""

    #On génère le formulaire
    f = AdminForm(username=username, password=password, email=mail)

    #On renvoie le template avec le formulaire
    return render_template("edit-adminBS.html", admin=u, form=f)




@app.route("/save/admin/", methods=("POST", ))
@login_required
def save_admin():
    """
    Fonction qui permet de créer/modifier un admin
    """

    #On récupère le formulaire
    f = AdminForm()

    #Si le nom d'utilisateur est vide, on affiche un message d'erreur
    if f.username.data == "":
        f.username.errors += ("Le nom d'utilisateur est obligatoire",)
        return render_template("edit-adminBS.html", form=f)

    #Si l'email est vide, on affiche un message d'erreur
    if f.email.data == "":
        f.email.errors += ("L'adresse email est obligatoire",)
        return render_template("edit-adminBS.html", form=f)

    #Si l'email est déjà utilisé, on affiche un message d'erreur
    if get_user_by_mail(f.email.data):
        f.email.errors += ("Cette adresse email est déjà utilisée",)
        return render_template("edit-adminBS.html", form=f)

    #On récupère l'utilisateur dans la db
    u = load_user(f.username.data)

    #Si l'utilisateur n'existe pas, on le crée
    if u is None:

        #Si le mot de passe est vide, on affiche un message d'erreur
        if f.password.data == "":
            f.password.errors +=  ("Mot de passe obligatoire",)
            return render_template("edit-adminBS.html", form=f, isWrong=True)

        #On crée un hash du mot de passe pour le stocker dans la db
        m = sha256()
        m.update(f.password.data.encode('utf-8'))

        #On crée l'utilisateur
        u = User(username=f.username.data,
                 password=m.hexdigest(),
                 email=f.email.data)

        #On ajoute l'utilisateur à la db
        db.session.add(u)

    #Si le formulaire est valide, on sauvegarde les modifications
    if f.validate_on_submit():

        #On met à jour ne nom d'utilisateur
        u.username = f.username.data

        #Si le mot de passe a été modifié (présent dans le formulaire), on met à jour le hash du mot de passe
        if f.password.data != "":
            m = sha256()
            m.update(f.password.data.encode('utf-8'))
            u.password = m.hexdigest()

        #On met à jour l'email
        u.email = f.email.data

        #On sauvegarde les modifications dans la db
        db.session.commit()

        #On redirige vers la page des administrateurs
        return redirect(url_for('admins'))

    #Sinon, on affiche le formulaire avec les erreurs
    return render_template("edit-adminBS.html", admin=u, form=f)




@app.route("/remove/admin/<username>")
@login_required
def remove_admin(username):
    """
    Fonction qui permet de supprimer un admin
    """

    #On récupère l'utilisateur dans la db
    u = load_user(username)

    #Si l'utilisateur n'existe pas, on renvoie une erreur 404
    if u is None:
        return abort(404)

    #On supprime l'utilisateur de la db
    db.session.delete(u)
    db.session.commit()

    #On redirige vers la page des administrateurs
    return redirect(url_for('admins'))

    #Commentaire inutile pour avoir pile 666 lignes de code (satanisme) :D