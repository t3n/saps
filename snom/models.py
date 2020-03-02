from django.db import models


class Phone(models.Model):
    phone_type = models.CharField(max_length=12)
    mac_address = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    pname = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    realname = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    uid = models.CharField(max_length=200, null=True, blank=True)
    outboundUrl = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.phone_type + '-' + self.mac_address
