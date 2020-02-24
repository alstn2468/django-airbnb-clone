from django.views import View
from django.shortcuts import render


class LoginView(View):
    """users application LoginView class

    Inherit             : View
    Templates name      : users/login.html
    """

    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        pass
