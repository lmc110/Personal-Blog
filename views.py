import flask
import models

from init import db, app

@app.route('/')
def index():
    return flask.render_template('index.html')




