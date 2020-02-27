from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('authorize', views.authorize, name='authorize'),
    path('me', views.me, name='me'),
    path('<str:phone_type>-<str:mac_address>.htm', views.phone),
    path('<str:phone_type>.htm', views.phone_type),
    path('<str:phone_type>/general.xml', views.general),
    path('<str:phone_type>/firmware.xml', views.firmware),
    path('<str:phone_type>/<str:mac_address>.xml', views.specific),
    path('admin/', admin.site.urls),
]
