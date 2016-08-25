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


@app.route('/logout')
def handle_logout():
    del flask.session['auth_user']
    return flask.redirect('/')


@app.route('/create')
def create_form():
    return flask.render_template('create_post.html')


@app.route('/create', methods=['POST'])
def handle_create():
    title = flask.request.form['title']
    text = flask.request.form['post-text']
    #add post to database
    post = models.Post()
    post.title = title
    post.body = text
    db.session.add(post)
    db.session.commit()
    pid = post.id
    return flask.redirect(flask.url_for('post_page', pid=pid), code=303)


@app.route('/posts/<int:pid>')
def post_page(pid):
    post = models.Post.query.get(pid)
    return flask.render_template('post.html', post=post)


