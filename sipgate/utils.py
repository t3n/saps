from django.contrib.auth.models import User

from authlib.integrations.django_client import OAuth

from .models import OAuth2Token


def fetch_token(name, request):
    token = OAuth2Token.objects.get(name=name, user=request.user)

    return token.to_token()


def update_token(name, token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.objects.get(name=name, refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.objects.get(name=name, access_token=access_token)
    else:
        return

    # update old token
    item.access_token = token["access_token"]
    item.refresh_token = token.get("refresh_token")
    item.expires_at = token["expires_at"]
    item.save()

    # Check if user is Staff
    userinfo = oauth.sipgate.get(
        "https://api.sipgate.com/v2/authorization/userinfo", token=token
    ).json()
    userdata = oauth.sipgate.get(
        "https://api.sipgate.com/v2/users/" + userinfo["sub"], token=token
    ).json()
    User.objects.filter(email=item.user).update(is_staff=userdata["admin"])


oauth = OAuth(fetch_token=fetch_token, update_token=update_token)
oauth.register(
    name="sipgate",
    access_token_url=(
        "https://login.sipgate.com"
        "/auth/realms/third-party/protocol/openid-connect/token"
    ),
    authorize_url=(
        "https://login.sipgate.com"
        "/auth/realms/third-party/protocol/openid-connect/auth"
    ),
    api_base_url="https://api.sipgate.com/v2",
    client_kwargs={"scope": "devices:read users:read"},
)


def get_credentials(request, user_id, device_id):
    for device in oauth.sipgate.get(
        "https://api.sipgate.com/v2/" + user_id + "/devices", request=request
    ).json()["items"]:
        if device["id"] == device_id:
            return device


def create_user(userdata):
    return User.objects.create_user(
        username=userdata["email"],
        email=userdata["email"],
        first_name=userdata["firstname"],
        last_name=userdata["lastname"],
        is_staff=userdata["admin"],
    )
