class BaseConfig(object):
    DEBUG = True
    TESTING = False
    MONGO_URI = 'mongodb://TODO'


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
