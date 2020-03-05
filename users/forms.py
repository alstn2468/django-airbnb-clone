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


class SignUpForm(forms.Form):
    """Users application signup form

    Inherit:
        forms.Form

    Field:
        first_name     : CharField
        last_name      : CharField
        email          : EmailField
        password       : CharField
        password_check : CharField

    Method:
        clean_email          : Check user exists with form email
        check_password_check : Check password is equal to password_check
        save                 : Create user object from cleaned_data
    """

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            User.objects.get(username=email)
            raise forms.ValidationError("User already exists with that email")
        except User.DoesNotExist:
            return email

    def clean_password_check(self):
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")

        if password != password_check:
            raise forms.ValidationError("Password confirmation does not match")

        return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
