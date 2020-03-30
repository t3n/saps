from django.contrib import admin

from .models import (
    Firmware,
    Language,
    Phone,
    PhoneType,
    FunctionKeys
)


admin.site.register(Firmware)
admin.site.register(Language)
admin.site.register(Phone)
admin.site.register(PhoneType)
admin.site.register(FunctionKeys)
