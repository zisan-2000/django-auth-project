from rest_framework import generics, permissions, status
from .models import ToDo
from .serializers import ToDoSerializer
from accounts.permissions import IsAdmin, IsUser, IsSuperAdmin  # ✅ import
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import CanApproveToDo, CanEditOthersToDo, CanDeleteOthersToDo


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
    permission_classes = [
        permissions.IsAuthenticated,
        CanEditOthersToDo,
        CanDeleteOthersToDo
    ]
    
    def get_queryset(self):
        user = self.request.user

        if user.role == 'super_admin':
            return ToDo.objects.all()

        elif user.role == 'admin':
            return ToDo.objects.filter(Q(user=user) | Q(user__admin=user))

        else:
            return ToDo.objects.filter(user=user)
        

class ApproveToDoView(APIView):
    permission_classes = [CanApproveToDo]

    def post(self, request, pk):
        try:
            todo = ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo not found"}, status=status.HTTP_404_NOT_FOUND)

        todo.completed = True
        todo.save()
        return Response({"message": "ToDo approved ✅"})