from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterUserView
from django.urls import path

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name = "register"),
    path("login/", TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name = "token_refresh"),
]
