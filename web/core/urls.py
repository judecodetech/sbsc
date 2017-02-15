from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url( r'^search/$', views.ajax_suspect_search, name = 'ajax_suspect_search' ),
]