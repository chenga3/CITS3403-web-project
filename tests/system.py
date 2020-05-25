import unittest, os, time
from app import db, create_app
from app.models import User
from config import TestConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver.exe'))
        if not self.driver:
            self.skipTest('Could not create driver')
        else:
            self.app = create_app(TestConfig)
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()
            users = User.query.all()
            print(users)
            if users:
                self.skipTest('Database is not empty')
            db.session.query(User).delete()
            u = User(username='admin', email='admin@admin.com', admin=True)
            u.set_password('pw')
            db.session.add(u)
            db.session.commit()
            self.driver.maximize_window()
    
    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()

    # tests a workflow where an admin logs in, navigates to the manage page,
    # adds a user, makes a mistake with the user's username and must edit the same user,
    # and then finally logs out
    def test_admin_manage_user(self):
        self.driver.get('http://localhost:5000/login')
        time.sleep(1)
        user_email_field = self.driver.find_element_by_id('user')
        password_field = self.driver.find_element_by_id('p0')
        submit = self.driver.find_element_by_id('submit')
        user = 'admin'
        pw = 'pw'
        
        # login as admin
        user_email_field.send_keys(user)
        password_field.send_keys(pw)
        submit.click()
        time.sleep(1)

        # check admin nav bar element and click on it
        admin_nav = self.driver.find_element_by_id('administration')
        self.assertIsNotNone(admin_nav)
        admin_nav.click()

        # click manage users button to display users via AJAX
        manageusers = self.driver.find_element_by_id('manageusers')
        manageusers.click()
        time.sleep(3)
        # check a table pops up
        thead = self.driver.find_element_by_tag_name('thead')
        self.assertIsNotNone(thead)

        # nav to add user page
        addbutton = self.driver.find_element_by_id('addbutton')
        addbutton.click()
        # add a user
        username = 'add'
        email = 'add@add.com'
        password = 'pw'
        password2 = 'pw'
        role = 'User'
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password2').send_keys(password2)
        role_select = Select(self.driver.find_element_by_id('role'))
        lang_select = Select(self.driver.find_element_by_id('prefer_language'))
        role_select.select_by_value('user')
        lang_select.select_by_value('py')
        self.driver.find_element(By.NAME, "adduser").click()
        # check for success flash message
        msg = self.driver.find_element_by_class_name('flash').get_attribute('innerHTML')
        self.assertEqual(msg, 'User successfully added.')

        # navigate back to manage page
        button1 = self.driver.find_element_by_class_name('button1')
        button1.click()
        time.sleep(2)
        # check a table pops up
        thead = self.driver.find_element_by_tag_name('thead')
        self.assertIsNotNone(thead)

        # edit the same user we just added
        u = User.query.filter_by(username=username).first()
        table_row = self.driver.find_element_by_id('user' + str(u.id))
        self.assertIsNotNone(table_row)
        table_row.find_element(By.CLASS_NAME, 'edit').click()
        # check current field entries match the data we entered earlier
        user_field = self.driver.find_element_by_id('username')
        current_user = user_field.get_attribute('value')
        email_field = self.driver.find_element_by_id('email')
        current_email = email_field.get_attribute('value')
        self.assertEqual(current_user, username)
        self.assertEqual(current_email, email)
        # change the username
        user_field.clear()
        user_field.send_keys('edit')
        self.driver.find_element(By.CLASS_NAME, 'button2').click()
        # confirm successful edit
        flash_msg = self.driver.find_element(By.CLASS_NAME, 'flash').get_attribute('innerHTML')
        self.assertEqual(flash_msg, 'User successfully updated.')
        # confirm successful edit on manage page
        self.driver.find_element(By.CLASS_NAME, 'button1').click()
        time.sleep(2)
        table_row = self.driver.find_element_by_id('user' + str(u.id))
        self.assertIsNotNone(table_row)
        tds = table_row.find_elements_by_tag_name('td')
        self.assertEqual(tds[0].get_attribute('innerHTML'), 'edit')

        # logout
        logout = self.driver.find_element_by_id('login').find_elements_by_tag_name('a')[1]
        self.assertIsNotNone(logout)
        logout.click()
        # check successful logout
        title = self.driver.find_elements_by_tag_name('h1')[1].get_attribute('innerHTML')
        self.assertEqual(title, 'Welcome')


if __name__ == '__main__':
    unittest.main(verbosity=2)