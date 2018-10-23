import os
from configparser import ConfigParser


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {"development": DevelopmentConfig,
              'testing': TestingConfig,
              'staging': StagingConfig,
              'production': ProductionConfig
              }


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for parameter in parameters:
            db[parameter[0]] = parameter[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db
