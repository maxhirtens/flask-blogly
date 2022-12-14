"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "boomerang"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

####### ROOT #######

@app.route('/')
def show_users():
  '''Show user list and signup form'''

  users = User.query.all()
  posts = Post.query.all()
  return render_template('list.html', users=users, posts=posts)

####### USERS #######

@app.route('/users/new', methods=['GET'])
def show_user_form():
  '''Show add user form'''

  return render_template('adduser.html')

@app.route('/users/new', methods=['POST'])
def add_user():
  '''Add a user and redirect home'''
  new_user = User(first_name = request.form['firstname'],
  last_name = request.form['lastname'],
  image_url=request.form['image'] or None
  )
  db.session.add(new_user)
  db.session.commit()

  return redirect('/')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
  '''Show user detail page'''

  user = User.query.get_or_404(user_id)
  return render_template('userdetail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
  '''Show edit user detail page'''

  user = User.query.get_or_404(user_id)
  return render_template('useredit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
  '''Take in new user form'''

  user = User.query.get_or_404(user_id)
  user.first_name = request.form['firstname']
  user.last_name = request.form['lastname']
  user.image_url = request.form['image'] or None

  db.session.add(user)
  db.session.commit()

  return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  '''Delete user from db'''

  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  return redirect('/')

####### POSTS #######

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
  '''Show post form for user'''

  user = User.query.get_or_404(user_id)
  return render_template('newpost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
  '''Add user posts'''

  user = User.query.get_or_404(user_id)
  new_post = Post(
  title = request.form['title'],
  content = request.form['content'],
  user_id = user_id
  )

  db.session.add(new_post)
  db.session.commit()

  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
  '''Show post detail page'''

  post = Post.query.get_or_404(post_id)
  return render_template('postdetail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_detail(post_id):
  '''Show edit post form'''

  post = Post.query.get_or_404(post_id)
  return render_template('postedit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post(post_id):
  '''Take in new post form'''

  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  db.session.add(post)
  db.session.commit()

  return redirect('/')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
  '''Delete post from db'''

  post = Post.query.get_or_404(post_id)

  db.session.delete(post)
  db.session.commit()

  return redirect('/')

####### TAGS #######

@app.route('/tags', methods=['GET'])
def show_tags():
  '''Show all tags'''

  tags = Tag.query.all()

  return render_template('showtags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_associated_posts(tag_id):
  '''Show all posts with this tag'''

  tag = Tag.query.get_or_404(tag_id)

  return render_template('tagdetail.html', tag=tag)

@app.route('/tags/new', methods=['GET'])
def show_tag_form():
  '''Show form to make a new tag'''

  return render_template('newtag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
  '''Form data > new tag'''

  new_tag = Tag(
    name = request.form['name']
    )

  db.session.add(new_tag)
  db.session.commit()

  return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def show_tag_detail(tag_id):
  '''Show tag details'''

  tag = Tag.query.get_or_404(tag_id)

  return render_template('edittag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def tag_edit_form(tag_id):
  '''Show tag edit form'''

  tag = Tag.query.get_or_404(tag_id)

  return render_template('edittag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
  '''Show tag edit form'''

  tag = Tag.query.get_or_404(tag_id)
  tag.name = request.form['name']

  db.session.add(tag)
  db.session.commit()

  return redirect('/')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tags(tag_id):
  '''Delete tags'''

  tag = Tag.query.get_or_404(tag_id)

  db.session.delete(tag)
  db.session.commit()

  return redirect('/')
