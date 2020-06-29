from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("sipgate.urls")),
    path("", include("snom.urls")),
    path("admin/", admin.site.urls),
]
