from django.http import HttpResponseBadRequest
from django.shortcuts import render

from .models import Phone
from .utils import mac_address_valid, phone_type_valid


def phone_type(request, phone_type):
    context = {
        'server': '192.168.23.144',
        'phone_type': phone_type,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, 'phonetype.xml', context)


def phone(request, phone_type, mac_address):
    context = {
        'server': '192.168.23.144',
        'mac': mac_address,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    if not mac_address_valid(mac_address):
        return HttpResponseBadRequest("MAC address not valid")

    phone = Phone.objects.filter(mac_address=mac_address)
    status = 200
    if not phone:
        phone = Phone(phone_type=phone_type, mac_address=mac_address)
        phone.save()
        status = 201

    return render(request, 'phone.xml', context, status=status)


def general(request, phone_type):
    context = {
        'server': '192.168.23.144',
        'phone_type': phone_type,
    }
    return render(request, 'general.xml', context, 'application/xml')


def specific(request, phone_type, mac_address):
    context = {
        'server': '192.168.23.144',
        'user_realname': 'test',
        'user_name': 'test',
        'user_host': 'test',
        'user_pname': 'test',
        'user_uid': 'test',
        'user_outbound': 'test',
    }
    return render(request, 'specific.xml', context, 'application/xml')


def firmware(request, phone_type):
    context = {
        'server': '192.168.23.144',
        'phone_type': phone_type,
    }
    return render(request, 'firmware.xml', context, 'application/xml')
