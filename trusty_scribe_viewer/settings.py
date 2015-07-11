import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '!2s##((ihj=i7-xgo0vhrwz+756)edwx204&$+e&ig@^mf%gn2'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ()
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = 'trusty_scribe_viewer.urls'
TEMPLATES = [{'BACKEND' : 'django.template.backends.django.DjangoTemplates',
              'DIRS' : ['trusty_scribe_viewer/templates']}]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
