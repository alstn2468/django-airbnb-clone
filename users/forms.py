from django import forms
from users.models import User


class LoginForm(forms.Form):
    """Users application login form

    Inherit:
        forms.Form

    Field:
        email    : EmailField
        password : CharField

    Method:
        clean_email    : return any users you use for email
        clean_password : pass
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(username=email)

            if user.check_password(password):
                return self.cleaned_data

            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

