from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist, Q

from .models import (
    Firmware,
    FunctionKey,
    Language,
    Phone,
    PhoneType,
    Setting,
)
from .utils import mac_address_valid, phone_type_valid, get_function_keys, save_fkey
from .forms import FunctionKeyForm


@login_required(login_url="login")
def function_keys(request, device_id):
    phone = None
    try:
        phone = Phone.objects.filter(user=request.user, device=device_id).first()
    except ObjectDoesNotExist:
        return redirect("sipgate:assign")

    if phone is None:
        return redirect("sipgate:assign")

    fkeys = get_function_keys(phone)

    form = FunctionKeyForm(request.POST or None, fkeys=fkeys)
    if form.is_valid():
        for (fkey, function) in form.function_keys():
            save_fkey(phone, fkey, function)
        return redirect("snom:function_keys", device_id)
    else:
        form = FunctionKeyForm(fkeys=fkeys)

    return render(request, "fkeys.html", {"form": form})


def phone_type(request, phone_type):
    context = {
        "server": get_current_site(request).domain,
        "phone_type": phone_type,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, "phonetype.xml", context)


def phone(request, phone_type, mac_address):
    context = {
        "server": get_current_site(request).domain,
        "phone_type": phone_type,
        "mac_address": mac_address,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    if not mac_address_valid(mac_address):
        return HttpResponseBadRequest("MAC address not valid")

    phone = Phone.objects.filter(mac_address=mac_address)
    status = 200
    if not phone:
        phone = Phone(
            phone_type=PhoneType.objects.get(phone_type=phone_type),
            mac_address=mac_address,
        )
        phone.save()
        status = 201

    return render(request, "phone.xml", context, status=status)


def general(request, phone_type):
    try:
        language = Language.objects.get(phone_type__phone_type=phone_type)
    except ObjectDoesNotExist:
        language = None

    try:
        firmware = Firmware.objects.get(phone_type__phone_type=phone_type)
    except ObjectDoesNotExist:
        firmware = None

    settings = Setting.objects.filter(
        Q(phone=None, phone_type=None)
        | Q(phone=None, phone_type__phone_type=phone_type)
    ).exclude(Q(key="update_policy") | Q(key="firmware_interval"))

    if firmware:
        firmware = Setting.objects.filter(
            Q(phone=None, phone_type=None)
            | Q(phone=None, phone_type__phone_type=phone_type)
        ).filter(Q(key="update_policy") | Q(key="firmware_interval"))

    context = {
        "server": get_current_site(request).domain,
        "phone_type": phone_type,
        "firmware": firmware,
        "language": language,
        "settings": settings,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, "general.xml", context, "application/xml")


def specific(request, phone_type, mac_address):
    phone = get_object_or_404(Phone, mac_address=mac_address)
    try:
        function_keys = FunctionKey.objects.filter(phone=phone.id).all()
    except ObjectDoesNotExist:
        function_keys = None

    settings = Setting.objects.filter(Q(phone=phone, phone_type=None)).exclude(
        Q(key="update_policy") | Q(key="firmware_interval")
    )

    context = {
        "server": get_current_site(request).domain,
        "user_realname": phone.realname,
        "user_name": phone.username,
        "user_host": phone.host,
        "user_pass": phone.password,
        "settings": settings,
        "function_keys": function_keys,
    }

    return render(request, "specific.xml", context, "application/xml")


def firmware(request, phone_type):
    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    firmware = get_object_or_404(Firmware, phone_type__phone_type=phone_type)
    context = {
        "firmware": firmware,
    }

    return render(request, "firmware.xml", context, "application/xml")
