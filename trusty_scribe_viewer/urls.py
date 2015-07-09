from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lab_notebook/$', views.lab_notebook, name='lab_notebook'),
    url(r'^files/(?P<path_string>[a-zA-Z0-9_. -/]+)$', views.files, name='files')
]
