import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'supersecreeetkey'
WTF_CRSF_ENAVLED = True
# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'blog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'team3member@gmail.com'
MAIL_PASSWORD = 'tiMa$232'

# flask-msearch will use table name as elasticsearch index name unless set
# __msearch_index__
MSEARCH_INDEX_NAME = 'msearch'
# simple,whoosh,elaticsearch, default is simple
MSEARCH_BACKEND = 'whoosh'
# auto create or update index
MSEARCH_ENABLE = True
# when backend is elasticsearch
ELASTICSEARCH = {"hosts": ["127.0.0.1:5000"]}
