import re

from django.db.models import ObjectDoesNotExist

from .models import PhoneType, FunctionKey


def phone_type_valid(phone_type):
    for p in PhoneType.objects.all():
        if p.phone_type == phone_type:
            return True

    return False


def mac_address_valid(mac_address):
    if re.match("[0-9a-f]{12}$", mac_address.lower()):
        return True
    return False


def get_function_keys(phone):
    fkey_count = PhoneType.objects.get(phone_type=phone.phone_type).function_keys
    fkeys = list(FunctionKey.objects.filter(phone=phone).order_by("fkey"))

    fkey_range = list(range(1, fkey_count + 1))
    for fkey in fkeys:
        fkey_range.remove(fkey.fkey)

    for i in fkey_range:
        fkeys.insert(i - 1, FunctionKey(phone=phone, fkey=i))

    return fkeys


def save_fkey(phone, fkey, kind, number):
    if kind:
        try:
            f = FunctionKey.objects.get(phone=phone, fkey=fkey)
        except ObjectDoesNotExist:
            f = FunctionKey()

        f.phone = phone
        f.fkey = fkey
        f.kind = kind
        f.number = number
        f.save()
    else:
        try:
            f = FunctionKey.objects.get(phone=phone, fkey=fkey)
        except ObjectDoesNotExist:
            pass
        else:
            f.delete()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
