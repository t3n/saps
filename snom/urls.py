from django.urls import path

from . import views

urlpatterns = [
    path("<str:phone_type>-<str:mac_address>.htm", views.phone, name="phone"),
    path("<str:phone_type>.htm", views.phone_type, name="phone_type"),
    path("<str:phone_type>/general.xml", views.general, name="general"),
    path("<str:phone_type>/firmware.xml", views.firmware, name="firmware"),
    path("<str:phone_type>/<str:mac_address>.xml", views.specific, name="specific"),
    path("fkeys", views.function_keys, name="function_keys"),
]
