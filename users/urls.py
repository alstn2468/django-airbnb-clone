from django.urls import path
from users.views import LoginView, log_out, SignUpView, complete_verification

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", log_out, name="logout"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", complete_verification, name="complete_verfication"),
]
