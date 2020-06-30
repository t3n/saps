from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from authlib.common.errors import AuthlibBaseError

from snom.models import Phone
from .forms import AssignForm
from .models import OAuth2Token
from .utils import get_credentials, oauth, create_user


def home(request):
    if request.user.is_authenticated is not True:
        return redirect("sipgate:login")
    else:
        return redirect("sipgate:me")


@user_passes_test(lambda u: u.is_staff, login_url="login")
def assign(request):
    if request.user.is_authenticated is not True:
        return redirect("sipgate:login")
    if request.user.is_staff is not True:
        return "Not Staff"

    users = []
    for user in oauth.sipgate.get(
        "https://api.sipgate.com/v2/users/", request=request
    ).json()["items"]:
        users.append((user["id"], user["firstname"] + " " + user["lastname"]),)

    form = AssignForm(request.POST or None, choices=users)
    if form.is_valid():
        credentials = get_credentials(request, form.cleaned_data["user"])
        userdata = oauth.sipgate.get(
            "https://api.sipgate.com/v2/users/" + form.cleaned_data["user"],
            request=request,
        ).json()
        user = User.objects.filter(email=userdata["email"]).first()
        if not user:
            user = create_user(userdata)
        Phone.objects.filter(pk=form.cleaned_data["phone"].id).update(
            user=User.objects.filter(email=userdata["email"]).first(),
            device=form.cleaned_data["device"],
            username=credentials["credentials"]["username"],
            password=credentials["credentials"]["password"],
            realname=credentials["alias"],
            host=credentials["credentials"]["sipServer"],
        )
        return redirect("sipgate:assign")
    else:
        form = AssignForm(choices=users)

    return render(request, "assign.html", {"form": form})


def device(request, user_id):
    devices = oauth.sipgate.get(
        "https://api.sipgate.com/v2/" + user_id + "/devices", request=request
    ).json()["items"]

    return render(request, "device.html", {"devices": devices})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse("sipgate:authorize"))
    return oauth.sipgate.authorize_redirect(request, redirect_uri)


def authorize(request):
    try:
        token = oauth.sipgate.authorize_access_token(request)
    except AuthlibBaseError:
        return redirect("sipgate:login")
    userinfo = oauth.sipgate.get(
        "https://api.sipgate.com/v2/authorization/userinfo", token=token
    ).json()
    userdata = oauth.sipgate.get(
        "https://api.sipgate.com/v2/users/" + userinfo["sub"], token=token
    ).json()

    user = User.objects.filter(email=userdata["email"]).first()
    if not user:
        user = create_user(userdata)

    sipgate_token = OAuth2Token.objects.filter(name="sipgate", user=user).first()
    if not sipgate_token:
        sipgate_token = OAuth2Token(
            name="sipgate",
            token_type=token["token_type"],
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_at=token["expires_at"],
            user=user,
        )
        sipgate_token.save()

    auth_login(request, user)

    return redirect("sipgate:me")


@login_required(login_url="login")
def me(request):
    try:
        userinfo = oauth.sipgate.get(
            "https://api.sipgate.com/v2/authorization/userinfo", request=request
        ).json()
    except (ObjectDoesNotExist, TypeError):
        return redirect("sipgate:login")
    userdata = oauth.sipgate.get(
        "https://api.sipgate.com/v2/users/" + userinfo["sub"], request=request
    ).json()

    devices = Phone.objects.filter(user__email=userdata["email"])
    context = {"userdata": userdata, "devices": devices}

    return render(request, "me.html", context)
