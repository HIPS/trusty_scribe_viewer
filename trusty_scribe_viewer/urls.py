from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lab_notebook/$', views.lab_notebook, name='lab_notebook'),
    url(r'^lab_notebook/(?P<max_entries>[0-9]+)/$', views.lab_notebook, name='lab_notebook'),
    url(r'^browse/(?P<sha>[a-f0-9]+)/(?P<path_str>[a-zA-Z0-9_. -/]*)$', views.browse, name='browse'),
    url(r'^diff/(?P<sha_1>[a-f0-9]+)/(?P<sha_2>[a-f0-9]+)/$', views.diff, name='diff'),
    url(r'^commit/(?P<sha>[a-f0-9]+)/$', views.commit, name='commit'),
]
