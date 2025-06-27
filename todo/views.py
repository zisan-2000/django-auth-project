from rest_framework import generics, permissions
from .models import ToDo
from .serializers import ToDoSerializer
from accounts.permissions import IsAdmin, IsUser, IsSuperAdmin  # ✅ import
from django.db.models import Q

class ToDoListCreateView(generics.ListCreateAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'super_admin':
            return ToDo.objects.all()

        elif user.role == 'admin':
            return ToDo.objects.filter(
                Q(user=user) | Q(user__admin=user)
            )

        else:
            # ✅ সাধারণ ইউজার → শুধু নিজের
            return ToDo.objects.filter(user=user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ToDoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'super_admin':
            return ToDo.objects.all()

        elif user.role == 'admin':
            return ToDo.objects.filter(user__assigned_admin=user)

        else:
            return ToDo.objects.filter(user=user)