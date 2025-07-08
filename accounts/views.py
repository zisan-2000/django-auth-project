# accounts/views.py

from rest_framework import viewsets,generics, permissions, status, serializers
from rest_framework.exceptions import PermissionDenied  # ✅ এই লাইনটি যোগ করুন
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated





from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from .models import User, Division, Station, Team
from .serializers import UserSerializer,RegisterSerializer, LoginSerializer, DivisionSerializer, StationSerializer, TeamSerializer,CustomTokenObtainPairSerializer

from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsSuperAdmin, IsAdmin, IsUser

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
            from_email=settings.DEFAULT_FROM_EMAIL,  # স্পষ্ট করে বলা হলো
            recipient_list=[user.email],
            fail_silently=False  # ✅ Debug এর জন্য এটা রাখা ভালো
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
        if user.role == 'super_admin':
            return User.objects.all()

        elif user.role == 'admin':
            return User.objects.filter(
                Q(admin=user) | Q(id=user.id),  # 🔁 direct admin
                division=user.division,  # 🔁 same division
                station=user.station     # 🔁 same station
            )
        
        else:  # সাধারণ ইউজার
            return User.objects.filter(id=user.id)

    def perform_create(self, serializer):  # ✅ এই মেথড এখানে লিখবেন
        user = self.request.user
        password = self.request.data.get('password')
        
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})
    
        if user.role == 'super_admin':
            serializer.save(password=password)  # ✅ hashed হবে
        elif user.role == 'admin':
            serializer.save(
                admin=user,
                division=user.division,
                station=user.station,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                password=password  # ✅ hashed হবে
            )

        else:
            raise PermissionDenied("You are not allowed to create users.")
        
    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

    # Superadmin সব আপডেট করতে পারে
        if user.role == 'superadmin':
            serializer.save()
    
    # Admin শুধু নিজের অধীনের user update করতে পারবে
        elif user.role == 'admin' and instance.admin == user:
            serializer.save()
    
    # অন্য কেউ update করতে পারবে না
        elif user == instance:
            serializer.save()  # নিজেকে update করার অনুমতি
        else:
            raise PermissionDenied("You can only update your own or your users' info.")

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if user.role == 'superadmin':
            return super().destroy(request, *args, **kwargs)

        elif user.role == 'admin' and instance.admin == user:
            return super().destroy(request, *args, **kwargs)

        elif user == instance:
            return super().destroy(request, *args, **kwargs)

        else:
            raise PermissionDenied("You can only delete your own or your users.")



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

@login_required
def social_login_success(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'email': user.email,
        'full_name': user.full_name,  # 🔁 এই লাইন fixed
    })

class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        permissions = user.get_all_permissions()
        return Response({
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "permissions": list(permissions),
            "canApprove": user.has_perm("todo.can_approve_todo"),
            "canEdit": user.has_perm("todo.change_todo"),
            "canDelete": user.has_perm("todo.delete_todo")
        })
