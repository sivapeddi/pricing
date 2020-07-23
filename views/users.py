from flask import Flask, Blueprint, request, session, url_for, render_template, redirect
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"{email}....{password}")

        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('.login_user'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('alerts.index'))
                # return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = ""
    return redirect(url_for('.login_user'))