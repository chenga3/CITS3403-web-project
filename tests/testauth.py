import unittest
from app import app, db
from app.models import User

class RegistrationCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        u = User(username='alice', email='alice@gmail.com', admin=False)
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def register(self, username, email, password, password2):
        data = {'username': username, 'email': email, 'password': password, 'password2': password2}
        return self.app.post('/register', data=data, follow_redirects=True)
    
    def test_valid_user_registration(self):
        response = self.register('bob', 'bob@gmail.com', 'password', 'password')
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        u = User.query.filter_by(username='bob').first()
        self.assertIsNotNone(u)
        self.assertEqual(u.username, 'bob')
        self.assertEqual(u.email, 'bob@gmail.com')
        self.assertTrue(u.check_password('password'))
        self.assertFalse(u.admin)

    def test_taken_username_registration(self):
        response = self.register('alice', 'alice2@gmail.com', 'password', 'password')
        self.assertIn(b'Please use a different username', response.data)
        # check we still have only one User with username 'alice'
        u = User.query.filter_by(username='alice').all()
        self.assertEqual(len(u), 1)
    
    def test_taken_email_registration(self):
        response = self.register('alice2', 'alice@gmail.com', 'password', 'password')
        self.assertIn(b'Please use a different email', response.data)
        u = User.query.filter_by(email='alice@gmail.com').all()
        self.assertEqual(len(u), 1)

    def test_unmatched_passwords_registration(self):
        response = self.register('bob', 'bob@gmail.com', 'password', 'password1')
        self.assertIn(b'Field must be equal to password', response.data)
        u = User.query.filter_by(username='bob').first()
        self.assertIsNone(u)
    
    def test_incomplete_registration(self):
        response = self.register('', 'bob@gmail.com', 'password', 'password')
        self.assertIn(b'This field is required', response.data)
        response = self.register('bob', '', 'password', 'password')
        self.assertIn(b'This field is required', response.data)
        response = self.register('bob', 'bob@gmail.com', '', 'password')
        self.assertIn(b'This field is required', response.data)
        response = self.register('bob', 'bob@gmail.com', 'password', '')
        self.assertIn(b'This field is required', response.data)

class LoginCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        u = User(username='alice', email='alice@gmail.com', admin=False)
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username_email, password):
        data = {'username_email': username_email, 'password': password}
        return self.app.post('/login', data=data, follow_redirects=False)

    def test_valid_login(self):
        response = self.login('alice', 'password')
        self.assertEqual(response.status_code, 302)

    def test_invalid_username_email_login(self):
        response = self.login('bob', 'password')
        self.assertIn(b'Incorrect username or email', response.data)

    def test_invalid_password_login(self):
        response = self.login('alice', 'incorrect')
        self.assertIn(b'Incorrect password', response.data)