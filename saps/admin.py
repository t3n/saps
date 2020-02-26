from django.contrib import admin

from .models import Assignments, Device, Phone

admin.site.register(Assignments)
admin.site.register(Device)
admin.site.register(Phone)
