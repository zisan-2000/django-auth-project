# accounts/views.py

from rest_framework import viewsets,generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from .models import User
from .serializers import UserSerializer,RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"http://127.0.0.1:8000/api/accounts/verify-email/{uid}/{token}/"
        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify your email: {link}",
            from_email=None,
            recipient_list=[user.email],
        )

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})
    

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_superuser:
            serializer.save()
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_superuser and request.user != user:
            return Response({"detail": "You can only delete your own account."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid UID'}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        return Response({'error': 'Invalid token'}, status=400)
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://127.0.0.1:8000/api/accounts/reset-password-confirm/{uid}/{token}/"
            send_mail(
                "Reset your password",
                f"Click to reset: {link}",
                None,
                [user.email]
            )
            return Response({"message": "Password reset link sent."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid UID'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=400)

        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response({'message': 'Password reset successful'})

