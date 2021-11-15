from project import db
from project.models import Review

db.create_all()

# insert data
db.session.add(Review(1, 1, 5))
db.session.add(Review(1, 2, 5))

# commit the changes
db.session.commit()
