from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from .models import Phone
from .utils import mac_address_valid, phone_type_valid


def phone_type(request, phone_type):
    context = {
        'server': get_current_site(request).domain,
        'phone_type': phone_type,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, 'phonetype.xml', context)


def phone(request, phone_type, mac_address):
    context = {
        'server': get_current_site(request).domain,
        'phone_type': phone_type,
        'mac_address': mac_address,
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
        'server': get_current_site(request).domain,
        'phone_type': phone_type,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, 'general.xml', context, 'application/xml')


def specific(request, phone_type, mac_address):
    e = Phone.objects.get(mac_address=mac_address)

    context = {
        'server': get_current_site(request).domain,
        'user_realname': e.realname,
        'user_name': e.username,
        'user_host': e.host,
        'user_pass': e.password,
    }

    if not Phone.objects.filter(mac_address=mac_address):
        raise Http404("Phone not found")

    return render(request, 'specific.xml', context, 'application/xml')


def firmware(request, phone_type):
    context = {
        'server': get_current_site(request).domain,
        'phone_type': phone_type,
    }

    if not phone_type_valid(phone_type):
        return HttpResponseBadRequest("Phone type not valid")

    return render(request, 'firmware.xml', context, 'application/xml')
