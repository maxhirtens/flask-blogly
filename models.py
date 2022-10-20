"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
  '''User class'''

  __tablename__ = 'users'

  id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

  first_name = db.Column(db.String(20),
                     nullable=False
                     )

  last_name = db.Column(db.String(30),
                     nullable=False
                     )

  image_url = db.Column(db.String(200),
                     nullable=True,
                     default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png'
                     )

  posts = db.relationship("Post", backref="user")

  def greet(self):
        """Greet using name."""

        return f"Thanks for logging in, {self.first_name} {self.last_name}"


class Post(db.Model):
  '''User posts'''

  __tablename__ = 'posts'

  id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

  title = db.Column(db.String(50),
                     nullable=False
                     )

  content = db.Column(db.String(200),
                     nullable=False
                     )

  created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Tag(db.Model):
  '''Tags database'''

  __tablename__ = 'tags'

  id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

  name = db.Column(db.Text,
                    unique=True)

  posts = db.relationship('Post', backref='tags')

class PostTag(db.Model):
      '''Tags that go on posts'''

      __tablename__ = 'post_tags'

      post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
      tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
