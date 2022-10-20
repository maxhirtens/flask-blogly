from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = True

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
  '''Test flask routes for users'''

  def setUp(self):
    '''add test user'''
    User.query.delete()

    max = User(first_name='Max', last_name='Hirtenstein')
    p1 = Post(title="Test Title", content='Test Content', user_id='1')
    db.session.add(max)
    db.session.add(p1)
    db.session.commit()

    self.user_id = max.id

  def tearDown(self):
    '''cleans up'''
    db.session.rollback()

  def test_list_users(self):
    with app.test_client() as client:
        resp = client.get("/")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Max', html)

  def test_user_form(self):
    with app.test_client() as client:
        resp = client.get("/user/new")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<form method="POST">', html)

  def test_show_user(self):
      with app.test_client() as client:
          resp = client.get(f"/{self.user_id}")
          html = resp.get_data(as_text=True)

          self.assertEqual(resp.status_code, 200)
          self.assertIn('<p>User: {{user.first_name}} {{user.last_name}}</p>', html)
