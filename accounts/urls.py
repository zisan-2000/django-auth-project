# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),  # ✅ Add this

]
