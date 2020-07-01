from django.contrib.auth.models import User
from django.db import models


class Phone(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    device = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    realname = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.phone_type.phone_type + "-" + self.mac_address


class Firmware(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.host + self.path + self.filename


class FunctionKey(models.Model):
    phone = models.ForeignKey("Phone", on_delete=models.CASCADE)
    fkey = models.IntegerField()
    function = models.CharField(max_length=25)

    class Meta:
        unique_together = (
            "phone",
            "fkey",
        )

    def __str__(self):
        return (
            self.phone.phone_type.phone_type
            + "-"
            + self.phone.mac_address
            + "-"
            + str(self.fkey)
        )


class Language(models.Model):
    phone_type = models.ForeignKey("PhoneType", on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.host + self.path + self.filename


class PhoneType(models.Model):
    phone_type = models.CharField(max_length=12)
    function_keys = models.IntegerField()

    def __str__(self):
        return self.phone_type
