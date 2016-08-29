from init import db, app


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    subtitle = db.Column(db.String())
    body = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=False))

db.create_all(app=app)
