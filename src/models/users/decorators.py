from functools import wraps

from src.app import app

from flask import request
from flask import session, redirect
from flask import url_for


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function


def requires_admin_access(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        print("APP CONFIG : {}".format(app.config['ADMINS']))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function
