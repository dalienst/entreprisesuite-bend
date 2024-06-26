from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import (
    UserDetailView,
    UserRegisterView,
    LogoutView,
    VerifyEmailView,
    UserListView,
    LoginView,
)


urlpatterns = [
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<str:id>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="user-list"),
]
