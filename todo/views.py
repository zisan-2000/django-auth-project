from rest_framework import generics, permissions, status
from .models import ToDo
from .serializers import ToDoSerializer
from accounts.permissions import IsAdmin, IsUser, IsSuperAdmin, SameDivisionPermission  # ✅ import
from todo.permissions import (
    CanEditOthersToDo,
    CanDeleteOthersToDo
)
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import CanApproveToDo, CanEditOthersToDo, CanDeleteOthersToDo

from guardian.shortcuts import assign_perm
from accounts.models import User
from rest_framework.permissions import IsAuthenticated




class ToDoListCreateView(generics.ListCreateAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'super_admin':
            return ToDo.objects.all()

        elif user.role == 'admin':
            return ToDo.objects.filter(
                Q(user=user) | Q(user__admin=user),
                user__division=user.division  # ✅ ABAC filter!
            )

        else:
            # ✅ সাধারণ ইউজার → শুধু নিজের division এর নিজের data
            return ToDo.objects.filter(
                user=user,
                user__division=user.division  # ✅ ABAC!
            )
        
    def perform_create(self, serializer):
        user = self.request.user
        todo = serializer.save(user=user)

        approve_user_id = self.request.data.get("approve_user_id")
        if approve_user_id:
            try:
                target_user = User.objects.get(id=approve_user_id)

                # ✅ Permission check
                if user.role == 'super_admin':
                    assign_perm("todo.can_approve_todo", target_user, todo)
                elif user.role == 'admin':
                    # admin only can give perm within their division/station
                    if target_user.division == user.division and target_user.station == user.station:
                        assign_perm("todo.can_approve_todo", target_user, todo)
                        print(f"Permission assigned to {target_user.email} for todo {todo.id}")

                # else: সাধারণ user permission দিতে পারবে না

            except User.DoesNotExist:
                pass

class ToDoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [
        IsAuthenticated,           # 🔐 Login check
        IsAdmin | IsSuperAdmin,    # 🔑 RBAC → Admin or Super Admin only
        SameDivisionPermission,    # 🧠 ABAC → user.division == todo.user.division
        CanEditOthersToDo,         # ✏️ Object permission (edit)
        CanDeleteOthersToDo        # 🗑️ Object permission (delete)
    ]
    
    def get_queryset(self):
        user = self.request.user

        if user.role == 'super_admin':
            return ToDo.objects.all()

        elif user.role == 'admin':
            return ToDo.objects.filter(
                Q(user=user) | Q(user__admin=user),
                user__division=user.division  # 🧠 ABAC: only own division
            )
        
        else:
            return ToDo.objects.filter(user=user)
        

class ApproveToDoView(APIView):
    permission_classes = [CanApproveToDo]

    def post(self, request, pk):
        try:
            todo = ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Response({"error": "ToDo not found"}, status=status.HTTP_404_NOT_FOUND)

          
    # 👇 Object-level permission check
        self.check_object_permissions(request, todo)

        todo.completed = True
        todo.save()
        return Response({"message": "ToDo approved ✅"}, status=status.HTTP_200_OK)