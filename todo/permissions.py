# todo/permissions.py

from rest_framework.permissions import BasePermission
from guardian.shortcuts import get_perms


class CanApproveToDo(BasePermission):
    def has_permission(self, request, view):
        # শুধু login check
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # object-level permission check
        return "can_approve_todo" in get_perms(request.user, obj)

class CanEditOthersToDo(BasePermission):
    def has_object_permission(self, request, view, obj):
        # নিজেরটা হলে সবসময় পারবে
        if obj.user == request.user:
            return True
        # অন্য কারো হলে permission লাগবে
        return request.user.has_perm("todo.can_edit_others_todo")

class CanDeleteOthersToDo(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return request.user.has_perm("todo.can_delete_others_todo")
