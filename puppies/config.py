import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'changeme'
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_LOCATION = 'puppies.log'
    SERVER_PORT = 5000
    SERVER_IP = '0.0.0.0'
    CLIENT_SECRETS_DIR = 'secrets/'


class DevConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    LOGGING_LEVEL = logging.WARNING
    SERVER_PORT = os.getenv('OPENSHIFT_PYTHON_PORT')
    SERVER_IP = os.getenv('OPENSHIFT_PYTHON_IP')
    CLIENT_SECRETS_DIR = os.getenv('OPENSHIFT_DATA_DIR')


def configure_app(app):
    config = {
    "Dev": "puppies.config.DevConfig",
    "Test": "puppies.config.TestConfig",
    "Prod": "puppies.config.ProdConfig"
    }
    env = os.getenv('PUPPIESAPP_ENV', None)
    app.config.from_object(config[env])
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)