import unittest
from app import app, db
from app.models import User

class UserModelCase(unittest.TestCase):
    def setUp(self):
        # use separate in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()
        u = User(id=0, username='bob123', email='bob123@gmail.com', admin=False)
        u.set_password('password1')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hash(self):
        u = User.query.get(0)
        u.set_password("password2")
        self.assertFalse(u.check_password("password1"))
        self.assertTrue(u.check_password("password2"))