from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url('^poll/new/$', views.poll_new, name='poll_new'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, {'template_name': 'user/login.html', 'redirect_authenticated_user': True}),
    url(r'^logout/$', views.logout_user, name='logout')
]