from django.urls import path
from users.views import LoginView, log_out, SignUpView

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", log_out, name="logout"),
    path("signup", SignUpView.as_view(), name="signup"),
]
