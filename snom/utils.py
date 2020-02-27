import re


def phone_type_valid(phone_type):
    phone_types = [
        'snom300',
        'snom320',
        'snom360',
        'snom370',
    ]

    for p in phone_types:
        if p == phone_type:
            return True

    return False


def mac_address_valid(mac_address):
    if re.match("[0-9a-f]{12}$", mac_address.lower()):
        return True
    return False
