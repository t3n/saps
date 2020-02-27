from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('authorize', views.authorize, name='authorize'),
    path('me', views.me, name='me'),
]
