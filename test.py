import unittest
from flask_testing import TestCase
from app import db, app

# from flask import url_for
from app.user.models import User
from app.blog.models import *


class BaseTestCase(TestCase):
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db',
                      SECRET_KEY='asfdsfsaaffdf', WTF_CSRF_ENABLED=False)
    db.drop_all()
    db.create_all()
    db.session.add_all([Category(name='Смартфони'),
                        Post(category_id=1, user_id=1, title='Test title',
                             content='Test content for test title'),
                        User(username='unit_tester_main',
                             email='unit_tester_main@gmail.com',
                             password='qwerTy#45'),
                        User(username='unit_tester_comment',
                             email='unit_tester_comment@gmail.com',
                             password='qwerTy#45'),
                        Post(category_id=1, user_id=2, title='Post for test '
                                                             'likes',
                             content='Test content(post for test likes)'),
                        ])
    db.session.commit()

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
                                        data={'email': 'unit_tester_main'
                                                       '@gmail.com',
                                              'password': 'qwerTy#45'},
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
                '<em class="card-title text-muted">'
                'unit_tester_main@gmail.com</em>'
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
                                        data={'email': 'unit_tester_main'
                                                       '@gmail.com',
                                              'password': 'qwerty345'},
                                        follow_redirects=True)
            self.assert200(response)
            self.assertMessageFlashed('Введено невірний пароль.',
                                      category='danger')
            self.assert401(self.client.get('auth/account'))

    def test6_create_post(self):
        with self.client:
            # db.session.add(Category(name='Смартфони'))
            # db.session.commit()

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

    # перевірка для нeавторизованого користувача
    def test7_access_to_comment_for_unauth_user(self):
        comment1 = Comment(user_id=1, post_id=1, text='Test comment')
        db.session.add(comment1)
        db.session.commit()
        response = self.client.get('/post/1',
                                   content_type='html/text')
        self.assert200(response)
        self.assertFalse(
            'Коментувати'
            in response.get_data(as_text=True)
        )
        self.assertFalse(
            'Надіслати'
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            'Авторизуйтесь, щоб мати можливість залишати коментарі.'
            in response.get_data(as_text=True)
        )
        # якщо користувач НЕ авторизований, він НЕ може видалити коментарі
        response = self.client.post('/comment/1/delete',
                                    follow_redirects=True)
        self.assert403(response)
        self.assertTrue(
            'Ви не маєте прав на видалення даного коментаря'
            in response.get_data(as_text=True)
        )
        # якщо користувач НЕ авторизований, він НЕ може додавати коментарі
        response = self.client.post('/post/1',
                                    data={'comment': 'Great comment!'},
                                    follow_redirects=True)
        self.assertTrue(
            'Авторизуйтесь, щоб мати можливість залишати коментарі.'
            in response.get_data(as_text=True)
        )

    # перевірка для авторизованого користувача
    def test8_access_to_comment_for_auth_user(self):
        response = self.client.post('/auth/login',
                                    data={
                                        'email': 'unit_tester_main@gmail.com',
                                        'password': 'qwerTy#45'},
                                    follow_redirects=True)
        self.assert200(response)
        self.assertMessageFlashed('Користувач успішно увійшов у свій '
                                  'аккаунт!', category='success')
        # якщо користувач авторизований, він може додавати коментарі
        response = self.client.post('/post/1',
                                    data={'comment': 'Great!'},
                                    follow_redirects=True)
        self.assertTrue(
            'Коментарі'
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            'Надіслати'
            in response.get_data(as_text=True)
        )
        self.assertFalse(
            'Авторизуйтесь, для того, щоб мати можливість писати коментарі'
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            'Great!'
            in response.get_data(as_text=True)
        )
        # якщо користувач авторизований, він може видалити коментарі
        self.assertTrue(
            'title="Видалити"'
            in response.get_data(as_text=True)
        )
        response = self.client.post('/comment/2/delete',
                                    follow_redirects=True)
        self.assert200(response)
        self.assertFalse(
            'Great!'
            in response.get_data(as_text=True)
        )

    # перевірка для нeавторизованого користувача
    def test9_access_to_like_for_unauth_user(self):
        response = self.client.get('/post/1',
                                   content_type='html/text')
        # print(response.get_data(as_text=True))
        self.assert200(response)
        response = self.client.get('/post/1/like',
                                   content_type='html/text')
        self.assert401(response)
        self.assertTrue(
            'The server could not verify that you are authorized to access '
            'the URL requested '
            in response.get_data(as_text=True)
        )

    # перевірка для нeавторизованого користувача
    def test10_access_to_like_for_auth_user(self):
        response = self.client.post('/auth/login',
                                    data={'email': 'unit_tester_main@gmail.'
                                                   'com',
                                          'password': 'qwerTy#45'},
                                    follow_redirects=True)
        self.assert200(response)
        self.assertMessageFlashed('Користувач успішно увійшов у свій '
                                  'аккаунт!', category='success')
        response = self.client.get('/post/1',
                                   content_type='html/text')
        self.assert200(response)
        # перевірка того, що користувач НЕ може оцінювати власні пости
        response = self.client.get('/post/1/like',
                                   content_type='html/text')
        self.assert403(response)
        self.assertTrue(
            'Ви не можете оцінювати власні публікації'
            in response.get_data(as_text=True)
        )
        # перевірка того, що користувач може оцінювати чужі пости
        response = self.client.get('/post/2/like',
                                   content_type='html/text')
        self.assertTrue(
            'You should be redirected automatically to target URL:'
            in response.get_data(as_text=True)
        )
        response = self.client.get('/post/2',
                                   content_type='html/text')
        # print(response.get_data(as_text=True))
        self.assert200(response)
        self.assertTrue(
            'class="bi" data-toggle="tooltip">1</a>'
            in response.get_data(as_text=True)
        )


if __name__ == '__main__':
    unittest.main()
