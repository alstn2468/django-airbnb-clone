from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class LoggedOutOnlyView(UserPassesTestMixin):
    """users application LoggedOutOnlyView

    Inherit : UserPassesTestMixin
    """

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("core:home"))