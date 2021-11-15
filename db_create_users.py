from project import db
from project.models import User

db.create_all()

# insert data
db.session.add(User("John Smith", "admin", "ad@min.com", "admin"))

# commit the changes
db.session.commit()
