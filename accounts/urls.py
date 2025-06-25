# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, UserViewSet,VerifyEmailView,PasswordResetRequestView,PasswordResetConfirmView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)



router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),  # ✅ Add this
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='reset-password-request'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  
]
