from django.urls import path
from users.views import (
    LoginView,
    log_out,
    SignUpView,
    UserProfileView,
    complete_verification,
    github_login,
    github_callback,
    kakao_login,
    kakao_callback,
)

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("login/github", github_login, name="github-login"),
    path("login/github/callback", github_callback, name="github-callback"),
    path("login/kakao", kakao_login, name="kakao-login"),
    path("login/kakao/callback", kakao_callback, name="kakao-callback"),
    path("logout", log_out, name="logout"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", complete_verification, name="complete_verfication"),
    path("<int:pk>", UserProfileView.as_view(), name="profile"),
]
