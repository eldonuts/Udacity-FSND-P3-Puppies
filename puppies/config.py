import logging
import os


config = {
    "Dev": "puppies.config.DevConfig",
    "Test": "puppies.config.TestConfig",
    "Prod": "puppies.config.ProdConfig"
}

env = os.getenv('PUPPIESAPP_ENV', None)

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'changeme'
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_LOCATION = 'puppies.log'


class DevConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    LOGGING_LEVEL = logging.WARNING


def configure_app(app):
    app.config.from_object(config[env])
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)