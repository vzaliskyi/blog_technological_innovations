import unittest
from flask_testing import TestCase
from app import db, create_app

import re

app = create_app()
app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db',
                  SECRET_KEY='asfdsfsaaffdf', WTF_CSRF_ENABLED=False)
# from flask import url_for
from app.user.models import User
from app.blog.models import Category, Post


class BaseTestCase(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        db.session.add_all([
            Category(name='Смартфони'),
            Category(name='Ноутбуки'),
            User(username='tester01',
                 email='tester01@gmail.com',
                 password='qwerTy#45'),
            User(username='unit_tester_comment',
                 email='unit_tester_comment@gmail.com',
                 password='qwerTy#45'),
            Post(category_id=1, user_id=1, title='Назва блогу 1',
                 content='text text text text'),
            Post(category_id=2, user_id=2, title='Назва блогу 2',
                 content='text text text text'),
            Post(category_id=1, user_id=1, title='Назва блогу 3',
                 content='text text text text'),
            Post(category_id=2, user_id=2, title='Назва блогу 4',
                 content='text text text text'),
            Post(category_id=1, user_id=1, title='Назва блогу 5',
                 content='text text text text'),
            Post(category_id=1, user_id=1, title='The Best blog12',
                 content='text text text text'),
            Post(category_id=1, user_id=1, title='Супер Найкращий блог12',
                 content='text text text text')])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestsPagination(BaseTestCase):

    def test_pag(self):
        post = db.session.query(Post).all()
        amount_post = len(post)
        amount_pag = (amount_post // 5)
        posts_on_last_page = amount_post - (5 * amount_pag)
        for i in range(1, amount_pag + 2):
            response = self.client.get(f'/?page={i}',
                                   content_type='html/text')
            self.assert200(response)
            posts_on_page = re.findall(
                r'<h2><a class="article-title" '
                r'href="/post/[\d]+">[\w\W]*?</a></h2>',
                response.get_data(as_text=True))
            # print(posts_on_page)
            if i != amount_pag + 1:
                self.assertEqual(len(posts_on_page), 5)
            else:
                self.assertEqual(len(posts_on_page), posts_on_last_page)


class TestsOutputByCategories(BaseTestCase):

    def test_output_by_category(self):
        post = db.session.query(Post).filter(Post.category_id==1).all()
        amount_post = len(post)
        # print(post[0].title)
        amount_pag = (amount_post // 5)
        posts_on_last_page = amount_post - (5 * amount_pag)
        amount_post_on_page = 5
        for i in range(1, amount_pag + 2):
            response = self.client.get(f'/category/{i}',
                                       content_type='html/text')
            posts_on_page = re.findall(
                    r'<h2><a class="article-title" '
                    r'href="/post/[\d]+">[\w\W]*?</a></h2>',
                    response.get_data(as_text=True))
            # print(posts_on_page)
            if i == amount_pag + 1:
                amount_post_on_page = posts_on_last_page

            for y in range(0, amount_post_on_page):
                self.assertTrue(post[((i - 1) * 5) + y].title, posts_on_page[y])