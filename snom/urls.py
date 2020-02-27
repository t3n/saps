from django.urls import path

from . import views

urlpatterns = [
    path('<str:phone_type>-<str:mac_address>.htm', views.phone),
    path('<str:phone_type>.htm', views.phone_type),
    path('<str:phone_type>/general.xml', views.general),
    path('<str:phone_type>/firmware.xml', views.firmware),
    path('<str:phone_type>/<str:mac_address>.xml', views.specific),
]
