from django.contrib import admin

from .models import Firmware, Phone, PhoneType


admin.site.register(Firmware)
admin.site.register(Phone)
admin.site.register(PhoneType)
