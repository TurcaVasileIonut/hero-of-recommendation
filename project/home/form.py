from flask_wtf import Form
from wtforms import TextField


class MessageForm(Form):
    """
    Creates the textbox for search
    """
    search = TextField('Search a book to review')
