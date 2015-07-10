from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lab_notebook/$', views.lab_notebook, name='lab_notebook'),
    url(r'^lab_notebook/(?P<max_entries>[0-9]+)/$', views.lab_notebook, name='lab_notebook'),
    url(r'^browse/(?P<path_string>[a-zA-Z0-9_. -/]+)$', views.browse, name='browse')
]
