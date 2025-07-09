# accounts/permissions.py

from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'


class AttributeMatchPermission(BasePermission):
    """
    Generic ABAC permission:
    user.<user_attr> == obj.<obj_attr>
    """

    user_attr = None
    obj_attr = None

    def has_object_permission(self, request, view, obj):
        if self.user_attr is None or self.obj_attr is None:
            return False  # Invalid setup

        user_value = getattr(request.user, self.user_attr, None)
        obj_value = self.get_nested_attr(obj, self.obj_attr)
        return user_value == obj_value

    def get_nested_attr(self, obj, attr_path):
        """
        Support dot-notation like 'user.division'
        """
        for attr in attr_path.split('.'):
            obj = getattr(obj, attr, None)
            if obj is None:
                break
        return obj
    
class SameDivisionPermission(AttributeMatchPermission):
    user_attr = 'division'
    obj_attr = 'user.division'

class SameStationPermission(AttributeMatchPermission):
    user_attr = 'station'
    obj_attr = 'user.station'

class SameTeamPermission(AttributeMatchPermission):
    user_attr = 'team'
    obj_attr = 'user.team'
