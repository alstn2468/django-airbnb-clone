from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import uuid


class User(AbstractUser):
    """Custom User Model

    Inherit:
        AbstractUser

    Fields:
        avatar         : ImageField
        gender         : CharField
        bio            : TextField
        birth_date     : DateField
        language       : CharField
        currency       : CharField
        is_superhost   : BooleanField
        email_verified : BooleanField
        email_secret   : CharField

    Methods:
        verify_email : Send an email for verify user
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    is_superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    def verify_email(self):
        if not self.email_verified:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            send_mail(
                "Verify Aribnb Account",
                f"Verify account, this is your secret: {secret}",
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
            )
            return True
        return False
