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

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            User.objects.get(username=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        pass
