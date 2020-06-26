from django import forms
from django.contrib.auth import password_validation
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

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "email", "autocomplete": "off"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "password"}
        )
    )

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


class SignUpForm(forms.ModelForm):
    """Users application signup form

    Inherit:
        forms.ModelForm

    Meta:
        model  : User
        fields : (first_name, last_name, email, password,)

    Field:
        password       : CharField
        password_check : CharField

    Method:
        clean_email          : Check user exist witj email field data
        clean_password_check : Check password is equal to password_check
        save                 : Create user object from cleaned_data
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "First Name",
                    "class": "first-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "Last Name",
                    "class": "last-name",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "email", "autocomplete": "off"}
            ),
        }

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "class": "password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_check = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Confirm Password",
                "class": "password-check",
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            User.objects.get(username=email)
            raise forms.ValidationError(
                "User already exists with that email", code="existing_user"
            )
        except User.DoesNotExist:
            return email

    def clean_password_check(self):
        password = self.cleaned_data.get("password")
        password_check = self.cleaned_data.get("password_check")

        if password != password_check:
            raise forms.ValidationError("Password confirmation does not match")

        try:
            password_validation.validate_password(password, self.instance)
            return password
        except forms.ValidationError as error:
            self.add_error("password", error)

    def save(self, *args, **kwargs):
        user = super().save(commit=False)

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user.username = email
        user.set_password(password)
        user.save()
