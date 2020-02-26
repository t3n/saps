from django.http import HttpResponse
from django.shortcuts import render, reverse
from authlib.integrations.django_client import OAuth

from .settings import SIPGATE_CLIENT_ID, SIPGATE_CLIENT_SECRET
from .models import Phone

oauth = OAuth()
oauth.register(
    name='sipgate',
    client_id=SIPGATE_CLIENT_ID,
    client_secret=SIPGATE_CLIENT_SECRET,
    access_token_url='https://login.sipgate.com/auth/realms/third-party/protocol/openid-connect/token',
    access_token_params=None,
    authorize_url='https://login.sipgate.com/auth/realms/third-party/protocol/openid-connect/auth',
    authorize_params=None,
    api_base_url='https://api.sipgate.com/v2',
    client_kwargs={'scope': 'all'},
)


def home(request):
    login_uri = reverse('login')
    return HttpResponse(f'<a href="{login_uri}">Login with Sipgate</a>')


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('info'))
    return oauth.sipgate.authorize_redirect(request, redirect_uri)


def info(request):
    token = oauth.sipgate.authorize_access_token(request)
    account = oauth.sipgate.get('https://api.sipgate.com/v2/account', token=token).json()

    response = HttpResponse()
    response.write('<h1>Hello ' + account['company'] + '</h1>')

    return response


def phone_type(request, phone_type):
    context = {
        'server': '192.168.23.144',
        'phone_type': phone_type,
    }
    return render(request, 'phonetype.xml', context)


def phone(request, phone_type, mac_address):
    context = {
        'server': '192.168.23.144',
        'mac': mac_address,
    }
    phone = Phone(phone_type=phone_type, mac_address=mac_address)
    phone.save()
    return render(request, 'phone.xml', context)


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
