from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("sipgate.urls", "sipgate"), namespace="sipgate")),
    path("", include(("snom.urls", "snom"), namespace="snom")),
    path("admin/", admin.site.urls),
]
