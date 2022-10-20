'''Put sample data into our db.'''
from app import app
from models import User, Post, Tag, PostTag, db

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add users
max = User(first_name='Max', last_name='Hirtenstein')
tom = User(first_name='Tom', last_name='Braider')
linda = User(first_name='Linda', last_name='Wall')

# Add test posts
p1 = Post(title='Test 1', content="Test 1 Content", user_id='3')
p2 = Post(title='Test 2', content="Test 2 Content", user_id='3')
p3 = Post(title='Test 3', content="Test 3 Content", user_id='1')

# Add test tags
t1 = Tag(name='funny')
t2 = Tag(name='cool')

# Add tags to posts
pt1 = PostTag(post_id=1, tag_id=2)
pt2 = PostTag(post_id=2, tag_id=1)

# Add new objects to session, so they'll persist
db.session.add_all([max, tom, linda])
db.session.add_all([p1, p2, p3])

# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add_all([t1, t2])
# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add_all([pt1, pt2])

# Commit--otherwise, this never gets saved!
db.session.commit()
