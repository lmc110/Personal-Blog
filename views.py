import flask
import models
import markdown
import math
import datetime

from markupsafe import Markup
from init import db, app


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def index(page):
    auth_user = flask.session.get('auth_user', None)
    #filter posts by posted date, most recent first
    posts = models.Post.query.order_by(models.Post.date.desc()).all()
    total_posts = len(posts)
    nextPage = False
    prevPage = False
    maxPost = page * 5
    minPost = maxPost - 5
    #get 5 posts for current page number
    posts = posts[minPost:maxPost]
    if maxPost < total_posts:
        nextPage = True
    if minPost > 0:
        prevPage = True

    if page <= 0:
        return flask.abort(code=404)
    if page > math.ceil(total_posts / 5) and page != 1:
        return flask.abort(code=404)

    return flask.render_template('index.html', auth_user=auth_user, posts=posts,
                                 total_posts=total_posts,
                                 maxPost=maxPost,
                                 minPost=minPost,
                                 page=page,
                                 nextPage=nextPage,
                                 prevPage=prevPage)


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
    subtitle = flask.request.form['subtitle']
    #add post to database
    post = models.Post()
    post.title = title
    post.body = text
    post.subtitle = subtitle
    post.date = datetime.datetime.now(tz=None)
    db.session.add(post)
    db.session.commit()
    pid = post.id
    return flask.redirect(flask.url_for('post_page', pid=pid), code=303)


@app.route('/posts/<int:pid>')
def post_page(pid):
    post = models.Post.query.get(pid)
    if post is None:
        return flask.abort(code=404)
    body = Markup(markdown.markdown(post.body, output_format='html5'))
    return flask.render_template('post.html', title=post.title,
                                 body=body,
                                 date=post.date)


@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template('404.html'), 404
