import flask
import models

from init import db, app


@app.route('/')
def index():
    auth_user = flask.session.get('auth_user', None)

    return flask.render_template('index.html')


@app.route('/login')
def login_form():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    user = flask.request.form['user']
    password = flask.request.form['password']
    if user == 'admin' and password == app.config['ADMIN_PASSWORD']:
        flask.session['auth_user'] = user
        return flask.redirect('/', code=303)
    else:
        flask.flash('Invalid username or password', 'error')
        return flask.render_template('login.html', state='bad')



