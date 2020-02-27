from django.contrib import admin

from .models import Assignments, Device, Phone, OAuth2Token

admin.site.register(Assignments)
admin.site.register(Device)
admin.site.register(Phone)
admin.site.register(OAuth2Token)
