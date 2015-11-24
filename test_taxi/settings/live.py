from .base import *  # NOQA
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_taxi',
        'USER': 'test_taxi',
        'PASSWORD': 'test_taxi',
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST_CHARSET': 'utf8',
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}
ALLOWED_HOSTS = ("threat.drivepixels.ru",)

