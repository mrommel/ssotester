from django.conf.urls import url

from . import views

app_name = 'tester'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^refresh/(?P<user_id>.+)$', views.refresh, name='refresh'),
    url(r'^status/(?P<user_id>.+)$', views.status, name='status'),
]
