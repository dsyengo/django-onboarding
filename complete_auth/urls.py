from django.urls import path, include
from .views import  LogoutView, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('login', LoginView.as_view(), name='auth_login'),
    path('logout', LogoutView.as_view(), name='auth_logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]