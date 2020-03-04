import re
from .models import PhoneType


def phone_type_valid(phone_type):
    for p in PhoneType.objects.all():
        if p.phone_type == phone_type:
            return True

    return False


def mac_address_valid(mac_address):
    if re.match("[0-9a-f]{12}$", mac_address.lower()):
        return True
    return False
