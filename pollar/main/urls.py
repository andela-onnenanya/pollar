from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url('^poll/new/$', views.poll_new, name='poll_new'),
]