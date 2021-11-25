import unittest
from flask_testing import TestCase
from app import db, app

# from flask import url_for
from app.user.models import User, Post, Category


class BaseTestCase(TestCase):
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db',
                      SECRET_KEY='asfdsfsaaffdf', WTF_CSRF_ENABLED=False)
    db.drop_all()
    db.create_all()

    def create_app(self):
        return app

    def test1_home_page(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TechBlog', response.data)
        self.assertTrue('Категорії' in response.get_data(as_text=True))

    # перевірка неавторизованого користувача
    def test2_access_for_unauth_user(self):
        response = self.client.get('/', content_type='html/text')
        self.assert200(response)
        self.assertTrue(
            'Увійти'
            in response.get_data(as_text=True)
        )
        self.assertFalse(
            'Мій профіль'
            in response.get_data(as_text=True)
        )
        # print(response.get_data(as_text=True))
        self.assert401(self.client.get('/auth/account'))
        self.assert401(self.client.get('/post/create'))

    # перевірка успішної реєстрації користувача
    def test3_user_successful_registration(self):
        with self.client:
            response = self.client.get('/auth/register')
            self.assert200(response)
            self.assertTrue('<legend class="border-bottom mb-4">'
                            'Реєстрація</legend>'
                            in response.get_data(as_text=True))
            response = self.client.post('/auth/register',
                                        data={'username': 'unit_tester1',
                                              'email': 'team3member@gmail.com',
                                              'password': '12345qaZ!',
                                              'confirm_password': '12345qaZ!'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertMessageFlashed('Користувач unit_tester1 успішно '
                                      'зареєстрований!', category='success')
            self.assert401(self.client.get('auth/account'))

    # перевірка сценарію неуспішної реєстрації користувача
    def test4_user_unsuccessful_registration(self):
        with self.client:
            response = self.client.get('/auth/register')
            self.assert200(response)
            self.assertTrue('<legend class="border-bottom '
                            'mb-4">Реєстрація</legend>' in
                            response.get_data(as_text=True))
            # передаємо невірні значення полів
            response = self.client.post('/auth/register',
                                        data={'username': 'unit_tester1',
                                              'email': 'team3membergmail.com',
                                              'password': 'qwert',
                                              'confirm_password': 'qwer'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # та опісля перевіряємо роботу валідаторів
            self.assertTrue('Користувач з таким іменем уже зареєстрований!'
                            in response.get_data(as_text=True))
            self.assertTrue('Некоректна email адреса!'
                            in response.get_data(as_text=True))
            self.assertTrue('Поле повинно бути довжиною від 3 до 30 симолів!'
                            in response.get_data(as_text=True))
            self.assertTrue('Пароль повинен містити великі та малі літери'
                            in response.get_data(as_text=True))
            self.assertTrue('Пароль повинен містити цифру'
                            in response.get_data(as_text=True))
            self.assertTrue(
                'Пароль повинен містити символ(не літеру і не цифру)'
                in response.get_data(as_text=True)
            )
            self.assertTrue('Паролі не збігаються!'
                            in response.get_data(as_text=True))
            self.assert401(self.client.get('auth/account'))

    # перевірка успшної авторизації користувача
    def test5_user_successful_login(self):
        with self.client:
            response = self.client.get('/auth/login')
            # response = self.client.get(url_for('user_bp_in.login'))
            self.assert200(response)
            self.assertTrue(
                '<legend class="border-bottom mb-4">Вхід</legend>' in
                response.get_data(as_text=True))
            response = self.client.post('/auth/login',
                                        data={'email': 'team3member@gmail.com',
                                              'password': '12345qaZ!'},
                                        follow_redirects=True)
            self.assert200(response)
            # redirect_url = url_for('/auth/login', next='/auth/account')
            # self.assertRedirects(response, redirect_url)
            self.assertMessageFlashed('Користувач успішно увійшов у свій '
                                      'аккаунт!', category='success')
            self.assertTrue(
                '<legend class="border-bottom mb-4">Інформація '
                'про мене</legend>' in response.get_data(as_text=True)
            )
            self.assertTrue(
                '<em class="card-title text-muted">team3member@gmail.com</em>'
                in response.get_data(as_text=True)
            )
            # користувач тепер має доступ до сторінки аккаунту
            self.assert200(self.client.get('auth/account'))

    # перевірка сценарію неуспішної авторизації
    def test6_user_unsuccessful_login(self):
        with self.client:
            response = self.client.get('/auth/login')
            # response = self.client.get(url_for('user_bp_in.login'))
            self.assert200(response)
            self.assertTrue(
                '<legend class="border-bottom mb-4">Вхід</legend>' in
                response.get_data(as_text=True))
            # якщо користувач вводить емейл, який не зареєстроваинй на сайті
            response = self.client.post('/auth/login',
                                        data={'email': 'team33memb@gmail.com',
                                              'password': '12345qaZ!'},
                                        follow_redirects=True)
            self.assert200(response)
            self.assertMessageFlashed('Користувач із вказаним емейлом не '
                                      'зареєстрований на сайті.',
                                      category='danger')
            self.assertFalse(
                '<legend class="border-bottom mb-4">Інформація '
                'про мене</legend>' in response.get_data(as_text=True))
            self.assertFalse(
                '<em class="card-title text-muted">team3member@gmail.com</em>'
                in response.get_data(as_text=True))
            self.assert401(self.client.get('auth/account'))

            # якщо користувач вводить просто некоректний емейл
            response = self.client.post('/auth/login',
                                        data={'email': 'team3membergmail.com',
                                              'password': '12345q!'},
                                        follow_redirects=True)
            self.assert200(response)
            self.assertTrue('Некоректна email адреса!'
                            in response.get_data(as_text=True))
            self.assert401(self.client.get('auth/account'))

            # якщо користувач вводить невірний пароль
            response = self.client.post('/auth/login',
                                        data={'email': 'team3member@gmail.com',
                                              'password': '12345q!'},
                                        follow_redirects=True)
            self.assert200(response)
            self.assertMessageFlashed('Введено невірний пароль.',
                                      category='danger')
            self.assert401(self.client.get('auth/account'))

    def test6_create_post(self):
        with self.client:
            db.session.add(Category(name='Смартфони'))
            db.session.commit()

            response = self.client.post('/auth/login',
                                        data={'email': 'team3member@gmail.com',
                                              'password': '12345qaZ!'},
                                        follow_redirects=True)
            self.assert200(response)

            response = self.client.get('/post/create')
            self.assert200(response)

            response = self.client.post('/post/create',
                                        data={'category': 1,
                                              'title': 'Post_tester22',
                                              'content': 'папаапsdfh '
                                                         'gchkfyukhklv'
                                                         'mccgfsdfbxcvbfhghf '
                                              }, follow_redirects=True)
            self.assert200(response)

            # print(response.get_data(as_text=True))

            self.assertMessageFlashed('Публікація успішно створена',
                                      category='success')
            self.assertTrue('<h3 class="text-center mb-0">Post_tester22</h3>'
                            in response.get_data(as_text=True)
                            )


if __name__ == '__main__':
    unittest.main()
