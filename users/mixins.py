from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOnlyView(UserPassesTestMixin):
    """users application LoggedOutOnlyView

    Inherit : UserPassesTestMixin
    """

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't access login page.")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    """users application LoggedInOnlyView

    Inherit : LoginRequiredMixin
    """

    login_url = reverse_lazy("users:login")


class EmailLoginOnlyView(UserPassesTestMixin):
    """users application EmailLoginOnlyView

    Inherit : UserPassesTestMixin
    """

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't access update password page.")
        return redirect(reverse("core:home"))
