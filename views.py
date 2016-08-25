import flask
import models

from init import db, app


@app.route('/')
def index():
    auth_user = flask.session.get('auth_user', None)

    return flask.render_template('index.html')




