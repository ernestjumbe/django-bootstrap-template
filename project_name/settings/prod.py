"""Settings for Production Server"""
from {{project_name}}.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    #('You', 'your@mail'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
]

VAR_ROOT = '/var/www/{{project_name}}'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'media')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{project_name}}',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INSTALLED_APPS += (
    #'gunicorn',
)

PREPEND_WWW = True

WSGI_APPLICATION = '{{project_name}}.wsgi.application'

LOGGING = {
    'version': 1,
}
