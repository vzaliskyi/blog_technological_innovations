from flask_testing import TestCase
import unittest
from app import db, app
from app.user.models import User


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db',
                          SECRET_KEY='asfdsfsaaffdf')
        db.create_all()
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User(username='tester007',
                            email='tester007@gmail.com', password='12345qaZ@'))
        db.session.commit()
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test1_home_page(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TechBlog', response.data)
        # print('-test1_home_page is done')

    def test2_user_registration(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<legend class="border-bottom '
                        'mb-4">Реєстрація</legend>' in response.get_data(
            as_text=True))
        response = self.client.post('/auth/register',
                                    data={'username': 'unittester1',
                                          'email': 'team3member@gmail.com',
                                          'password': '12345qaZ!',
                                          'confirm_password': '12345qaZ!'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'Користувач unittester1 успішно зареєстрований!'
            in response.get_data(as_text=True))

    def test3_user_login(self):
        with self.client:
            response = self.client.get('/auth/login')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                '<legend class="border-bottom mb-4">Вхід</legend>' in
                response.get_data(as_text=True))
            response = self.client.post('/auth/login',
                                        data={'email': 'tester007@gmail.com',
                                              'password': '12345qaZ@'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = self.client.get('auth/account')
            self.assertTrue(
                '<em class="card-title text-muted">tester007@gmail.com</em>'
                in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
