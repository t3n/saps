from django.contrib import admin

from .models import (
    Firmware,
    Language,
    Phone,
    PhoneType,
    FunctionKey,
)


admin.site.register(Firmware)
admin.site.register(Language)
admin.site.register(Phone)
admin.site.register(PhoneType)
admin.site.register(FunctionKey)
