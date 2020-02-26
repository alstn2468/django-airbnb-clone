from django.views import View
from django.shortcuts import render
from users.forms import LoginForm


class LoginView(View):
    """users application LoginView class

    Inherit             : View
    Templates name      : users/login.html
    """

    def get(self, request):
        form = LoginForm()

        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        return render(request, "users/login.html", {"form": form})

