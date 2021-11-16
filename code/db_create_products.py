from project import db
from project.models import Product

db.create_all()

# insert data
db.session.add(Product("Pride and Prejudice", "Jane Austen", "1813", "Books", "Classic"))
db.session.add(Product("To Kill a Mockingbird", "Harper Lee", "1960", "Books", "Classic"))
db.session.add(Product("Crime and Punishment", "Fyodor Dostoevsky", "1866", "Books", "Classic"))
db.session.add(Product("The Call of the Wild", "Jack London", "1903", "Books", "Classic"))
db.session.add(Product("Buddenbrooks", "Thomas Mann", "1901", "Books", "Classic"))

# commit the changes
db.session.commit()
