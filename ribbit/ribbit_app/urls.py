from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^ribbits$', views.public, name='public'),
    url(r'^users/$', views.users, name='gen_users'),
    url(r'^users/(?P<username>\w{0,30})/$', views.users, name='specific_user'),
    url(r'^follow$', views.follow, name='follow'),
]