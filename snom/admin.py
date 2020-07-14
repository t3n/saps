from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from .models import (
    Firmware,
    FunctionKey,
    Language,
    Phone,
    PhoneType,
    Setting,
)


class AssignListFilter(SimpleListFilter):
    title = "Assignment"

    parameter_name = "Assignment"

    def lookups(self, request, model_admin):
        return (
            ("1", _("assigned"),),
            ("0", _("unassined"),),
        )

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(user=None)
        if self.value() == "1":
            return queryset.exclude(user=None)
        return queryset


@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ("phone_type", "url")
    fieldsets = (
        (None, {"fields": ["phone_type"]}),
        ("URL", {"fields": ["host", "path", "filename"]}),
    )


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")
    list_filter = (AssignListFilter,)
    fieldsets = (
        ("Phone", {"fields": ["phone_type", "mac_address", "user"]}),
        (
            "Sipgate",
            {
                "classes": ["collapse"],
                "fields": ["device", "username", "password", "realname", "host"],
            },
        ),
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("phone_type", "url")
    fieldsets = (
        (None, {"fields": ["phone_type"]}),
        ("URL", {"fields": ["host", "path", "filename"]}),
    )


@admin.register(PhoneType)
class PhoneTypeAdmin(admin.ModelAdmin):
    list_display = ("phone_type", "function_keys")


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("kind", "key", "value")
    fieldsets = (
        ("Kind", {"fields": ["phone_type", "phone"]}),
        ("Setting", {"fields": ["key", "value", "perm"]}),
    )


@admin.register(FunctionKey)
class FunctionKeyAdmin(admin.ModelAdmin):
    list_display = ("phone", "fkey", "kind", "number")
    ordering = ["phone", "fkey"]
