from {{ project_name }}.settings.base import *  # pylint: disable=W291,E202

DEBUG = True
TEMPLATE_DEBUG = True

VAR_ROOT = '/var/www/{{ project_name }}.com'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{project_name}}',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
        'HOST': '',
    }
}

# WSGI_APPLICATION = '{{ project_name }}.wsgi.dev.application'
