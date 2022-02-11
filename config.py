import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite3')
    JWT_SECRET_KEY = "SUPA_DUPA_SECRET_KEY"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True


config_by_name = dict(
    development=DevConfig,
    production=Config,
    default=Config,
)
