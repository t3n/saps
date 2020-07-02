from django.contrib import admin

from .models import (
    Firmware,
    FunctionKey,
    Language,
    Phone,
    PhoneType,
    Setting,
)


admin.site.register(Firmware)
admin.site.register(FunctionKey)
admin.site.register(Language)
admin.site.register(Phone)
admin.site.register(PhoneType)
admin.site.register(Setting)
