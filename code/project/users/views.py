import bcrypt
from flask import render_template, redirect, url_for, request, flash, Blueprint
from project.models import User, bcrypt
from flask_login import login_user, login_required, logout_user

from project.users.form import LoginForm, RegisterForm
from project import db


users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


# login page
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Take the username and password from the user and decide if they are valid data for an account
    """
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #login button was pressed
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('You were logged in')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    """ Disconnects the user from account, redirecting him to login page"""
    logout_user()
    flash('You were just logged out')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register/', methods=['GET', 'POST'])   # pragma: no cover
def register():
    """
    Takes data from Register Form and creates a new account if the data represents the possible data of a valid account
    If a new account was created, the user is redirected to home page, otherwise to register page
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # create a User object
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # add user in the database
        db.session.add(user)
        db.session.commit()
        login_user(user)
        # if the account was created, the user is redirected to home page
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)
