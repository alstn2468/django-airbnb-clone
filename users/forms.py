from django import forms


class LoginForm(forms.Form):
    """Users application login form

    Inherit:
        forms.Form

    Field:
        email    : EmailField
        password : CharField
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
