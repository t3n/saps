from django.db import models
from django.contrib.auth.models import User


class Phone(models.Model):
    phone_type = models.CharField(max_length=12)
    mac_address = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone_type + '-' + self.mac_address


class Device(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    sip_server = models.CharField(max_length=80)
    outbound_proxy = models.CharField(max_length=80)


class Assignments(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class OAuth2Token(models.Model):
    name = models.CharField(max_length=40)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_at = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )
