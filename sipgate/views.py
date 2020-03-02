from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.shortcuts import reverse
from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from django.shortcuts import render
from .forms import AssignForm
from .models import OAuth2Token
from snom.models import Phone


def fetch_token(name, request):
    token = OAuth2Token.objects.get(
        name=name,
        user=request.user
    )

    return token.to_token()


def update_token(name, token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.objects.get(name=name, refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.objects.get(name=name, access_token=access_token)
    else:
        return

    # update old token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    item.save()


oauth = OAuth(fetch_token=fetch_token, update_token=update_token)
oauth.register(
    name='sipgate',
    access_token_url='https://login.sipgate.com/auth/realms/third-party/protocol/openid-connect/token',
    authorize_url='https://login.sipgate.com/auth/realms/third-party/protocol/openid-connect/auth',
    api_base_url='https://api.sipgate.com/v2',
    client_kwargs={'scope': 'all'},
)


def home(request):
    login_uri = reverse('login')
    return HttpResponse(f'<a href="{login_uri}">Login with Sipgate</a>')


def get_credentials(request, user_id):
    return oauth.sipgate.get('https://api.sipgate.com/v2/' + user_id + "/devices", request=request).json()['items'][0]


def assign(request):
    users = []

    for user in oauth.sipgate.get('https://api.sipgate.com/v2/app/users/', request=request).json()['items']:
        users.append((user['id'], user['firstname'] + " " + user['lastname']),)

    if request.method == 'POST':
        form = AssignForm(request.POST, choices=users)
        if form.is_valid():
            credentials = get_credentials(request, form.cleaned_data['user'])
            Phone.objects.filter(pk=form.cleaned_data['phones'].id).update(
                username=credentials['credentials']['username'],
                password=credentials['credentials']['password'],
                realname=credentials['alias'],
                host=credentials['credentials']['sipServer']
            )
    else:
        form = AssignForm(choices=users)
    return render(request, 'assign.html', {'form': form})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('authorize'))
    return oauth.sipgate.authorize_redirect(request, redirect_uri)


def authorize(request):
    token = oauth.sipgate.authorize_access_token(request)
    userinfo = oauth.sipgate.get('https://api.sipgate.com/v2/authorization/userinfo', token=token).json()
    userdata = oauth.sipgate.get('https://api.sipgate.com/v2/users/' + userinfo['sub'], token=token).json()

    user = User.objects.filter(email=userdata['email']).first()
    if not user:
        user = User.objects.create_user(
            username=userdata['email'],
            email=userdata['email'],
            first_name=userdata['firstname'],
            last_name=userdata['lastname'],
            is_staff=userdata['admin']
        )

    sipgate_token = OAuth2Token.objects.filter(name='sipgate', user=user).first()
    if not sipgate_token:
        sipgate_token = OAuth2Token(
            name='sipgate',
            token_type=token['token_type'],
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            expires_at=token['expires_at'],
            user=user,
        )
        sipgate_token.save()

    response = HttpResponse()
    response.write('<h1>Hello ' + userdata['email'] + '</h1>')
    auth_login(request, user)

    return response


def me(request):
    userinfo = oauth.sipgate.get('https://api.sipgate.com/v2/authorization/userinfo', request=request).json()
    userdata = oauth.sipgate.get('https://api.sipgate.com/v2/users/' + userinfo['sub'], request=request).json()

    response = HttpResponse()
    response.write('<h1>Hello ' + userdata['email'] + '</h1>')

    return response
