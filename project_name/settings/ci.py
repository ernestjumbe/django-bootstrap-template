from {{project_name}}.settings.base import *  # pylint: disable=W291,E202
from {{project_name}}.settings.secrets import *

DEBUG = True
TEMPLATE_DEBUG = True

VAR_ROOT = '/var/www/{{project_name}}.com'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{project_name}}test',
        'USER': 'postgres',
        #'PASSWORD': 'db_password',
        #'PORT': 'port',
        #'HOST': 'localhost',
    }
}

# WSGI_APPLICATION = '{{project_name}}.wsgi.dev.application'
