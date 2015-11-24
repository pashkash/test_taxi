from .base import *  # NOQA
DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_taxi',
        'USER': 'root',
        'PASSWORD': 'kawai2006',
        'HOST': 'localhost',
        'PORT': '',
        'TEST_CHARSET': 'utf8',
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}
