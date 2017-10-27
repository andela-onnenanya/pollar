from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^polls/$', views.polls, name='polls'),
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls_view, name='polls_view'),
    url(r'^api/polls/(?P<poll_id>\d+)/$', views.votes, name='add_vote'),
    url('^polls/new/$', views.poll_new, name='poll_new'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, {'template_name': 'user/login.html', 'redirect_authenticated_user': True}),
    url(r'^logout/$', views.logout_user, name='logout')
]