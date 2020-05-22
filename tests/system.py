import unittest, os, time
from app import app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver.exe'))
        if not self.driver:
            self.skipTest
        else:
            db.init_app(app)
            db.create_all()
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

    def test_admin_manage_user(self):
        self.driver.get('http://localhost:5000/login')
        time.sleep(1)
        user_email_field = self.driver.find_element_by_id('user')
        password_field = self.driver.find_element_by_id('p0')
        submit = self.driver.find_element_by_id('submit')

        # login as admin
        user_email_field.send_keys('admin')
        password_field.send_keys('pw')
        submit.click()
        time.sleep(1)

        # check admin nav bar element and click on it
        admin_nav = self.driver.find_element_by_id('administration')
        self.assertIsNotNone(admin_nav)
        admin_nav.click()

        # nav to add user page
        add_user = self.driver.find_element(By.CLASS_NAME, "button1")
        add_user.click()

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

        # edit the same user
        table_row = self.driver.find_element_by_id(username)
        self.assertIsNotNone(table_row)
        table_row.find_element(By.CLASS_NAME, 'edit').click()

        user_field = self.driver.find_element_by_id('username')
        current_user = user_field.get_attribute('value')
        email_field = self.driver.find_element_by_id('email')
        current_email = email_field.get_attribute('value')
        self.assertEqual(current_user, username)
        self.assertEqual(current_email, email)
        user_field.clear()
        user_field.send_keys('edit')

        self.driver.find_element(By.CLASS_NAME, 'button2').click()

        # confirm successful edit
        flash_msg = self.driver.find_element(By.CLASS_NAME, 'flash').get_attribute('innerHTML')
        self.assertEqual(flash_msg, 'User successfully updated.')

        self.driver.find_element(By.CLASS_NAME, 'button1').click()
        table_row = self.driver.find_element_by_id('edit')
        self.assertIsNotNone(table_row)


if __name__ == '__main__':
    unittest.main(verbosity=2)