from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignUpForm
from users.models import User

import os
import requests


class LoginView(FormView):
    """users application LoginView class

    Inherit       : FormView
    template_name : "users/login.html"
    form_class    : LoginForm
    success_url   : reverse_lazy("core:home")

    Method:
        form_valid : user auth process
    """

    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


def log_out(request):
    logout(request)

    return redirect(reverse("core:home"))


class SignUpView(FormView):
    """users application SignUpView class

    Inherit       : FormView
    template_name : users/signup.html
    form_class    : SignUpForm
    success_url   : reverse_lazy("core:home")

    Method:
        form_valid : Create user using save method and login user
    """

    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # To do : add succes message
    except User.DoesNotExist:
        # To do : add error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")

    redirect_url = "http://127.0.0.1:8000/users/login/github/callback"
    query_string = (
        f"?client_id={client_id}" + f"&redirect_url={redirect_url}" + "&scope=read:user"
    )
    return redirect(f"https://github.com/login/oauth/authorize" + query_string)


def github_callback(request):
    code = request.GET.get("code", None)
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")

    if code is not None:
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        result_json = response.json()
        error = result_json.get("error", None)

        if error:
            return redirect(reverse("users:login"))

        access_token = result_json.get("access_token")
        api_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = api_request.json()
        username = profile_json.get("login", None)

        if not username:
            return redirect(reverse("users:login"))

        name = profile_json.get("name")
        email = profile_json.get("email")
        bio = profile_json.get("bio")
        user = User.objects.get(email=email)

        if user:
            return redirect(reverse("users:login"))

        user = User.objects.create(
            username=email, first_name=name, bio=bio, email=email
        )
        login(request, user)

    return redirect(reverse("core:home"))
