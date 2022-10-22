import email
from .app import db

from flask_login import UserMixin
from .app import login_manager

class Author(db.Model):
    """
    Class Author avec id et name 
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)

class Book(db.Model):
    """
    Class Book avec id, title, price, url, img, author_id
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)
    url = db.Column(db.String(1024))
    img = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy="dynamic"))

    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)


class User(db.Model, UserMixin):
    """
    Class User avec id, username, password, email
    """
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120))

    def get_id(self):
        return self.username


########################################
# Méthodes de récupération des données #
########################################


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def get_sample(page=1):
    books = Book.query.all()
    length = len(books)
    isFirst = False
    isLast = False

    if page <= 1:
        page = 1
        isFirst = True

    if page >= (length/12):
        page = int(length/12) +1
        isLast = True
        selected_books = books[(page-1)*12:]
    else:
        selected_books = books[(page-1)*12:page*12]


    return selected_books, page, isFirst, isLast


def get_authors():
    return Author.query.order_by(Author.name).all()

def get_author(id):
    return Author.query.get_or_404(id)

def get_book_details(id):
    return Book.query.get(id)

def get_books_by_author(author_id):
    return Book.query.filter_by(author_id=author_id).all()

def get_users():
    return User.query.all()

def get_user_by_mail(mail):
    return User.query.filter_by(email=mail).first()