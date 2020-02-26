from django.db import models


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
