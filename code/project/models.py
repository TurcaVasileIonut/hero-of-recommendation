from project import db
from project import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model):
    """
    Creates the database for users
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    reviews = relationship("Review", backref="author")

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<name - {}>'.format(self.name)


class Product(db.Model):
    """
    Creates the database for products
    """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String)
    author = db.Column(db.String)
    points = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    reviews = relationship("Review", backref="product")

    def __init__(self, name, author, year, department, category):
        self.name = name
        self.author = author
        self.year = year
        self.points = int(0)
        self.department = department
        self.category = category

    def __repr__(self):
        return '{}'.format(self.id)


class Review(db.Model):
    """
    Creates the database for reviews
    """
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    product_id = db.Column(db.Integer, ForeignKey('products.id'))
    grade = db.Column(db.Integer, nullable=False)

    def __init__(self, author, product, grade):
        self.author_id = author
        self.product_id = product
        self.grade = grade

    def __repr__(self):
        return '{}-{}-{}'.format(self.author_id, self.product_id, self.grade)
