from django.urls import path
from users.views import LoginView, log_out

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", log_out, name="logout"),
]
