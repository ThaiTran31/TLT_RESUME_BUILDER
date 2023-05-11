from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path("register/", views.RegisterUserAPIView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.BlackListTokenView.as_view(), name="blacklist_token"),
    path("user-details/", views.UserDetails.as_view(), name="user-details"),
    path("user-profile-update/<int:pk>/", views.UserProfileUpdate.as_view(), name="user-profile-update"),
    # path("google-authen/", views.GoogleAuthenticate.as_view(), name="google-authen"),
    # path("linkedin-authen/", views.UserDetails.as_view(), name="linkedin-authen"),
]
