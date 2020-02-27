from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('authorize', views.authorize, name='authorize'),
    path('me', views.me, name='me'),
    path('snom/', include('snom.urls')),
    path('admin/', admin.site.urls),
]
