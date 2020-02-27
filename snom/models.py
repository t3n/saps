from django.db import models


class Phone(models.Model):
    phone_type = models.CharField(max_length=12)
    mac_address = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone_type + '-' + self.mac_address
