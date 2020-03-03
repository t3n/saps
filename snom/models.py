from django.db import models


class Phone(models.Model):
    phone_type = models.ForeignKey('PhoneType', on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    realname = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.phone_type.phone_type + '-' + self.mac_address


class Firmware(models.Model):
    phone_type = models.ForeignKey('PhoneType', on_delete=models.CASCADE)
    firmware = models.CharField(max_length=25)

    def __str__(self):
        return self.phone_type.phone_type + '-' + self.firmware


class PhoneType(models.Model):
    phone_type = models.CharField(max_length=12)
    
    def __str__(self):
        return self.phone_type
