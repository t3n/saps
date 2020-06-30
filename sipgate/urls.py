from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("authorize", views.authorize, name="authorize"),
    path("me", views.me, name="me"),
    path("assign", views.assign, name="assign"),
    re_path(r"device/(?P<user_id>\w{1,5})/$", views.device, name="device"),
]
