'''Project config'''


import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'postgres://urlshortener:qwerty123@localhost:5432/urlshortener'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'gF1tGr6Rh75P+u4rEouCisLm4/3iQUGSDQYuWEfcwRw='
