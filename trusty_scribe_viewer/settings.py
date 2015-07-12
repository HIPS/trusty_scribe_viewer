import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '!2s##((ihj=i7-xgo0vhrwz+756)edwx204&$+e&ig@^mf%gn2'
DEBUG = True
ALLOWED_HOSTS = []
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = 'trusty_scribe_viewer.urls'
TEMPLATES = [{'BACKEND' : 'django.template.backends.django.DjangoTemplates',
              'DIRS' : [os.path.join(BASE_DIR, 'trusty_scribe_viewer/templates')]}]
STATIC_URL = '/static/'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
