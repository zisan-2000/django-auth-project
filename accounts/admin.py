# accounts/admin.py

from django.contrib import admin
from .models import User, Division, Station, Team  # ✅ নতুন মডেলগুলো import

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'full_name')

    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password', 'role', 'admin', 'division', 'station', 'team')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )

# ✅ রেজিস্টার করুন
admin.site.register(User, UserAdmin)
admin.site.register(Division)
admin.site.register(Station)
admin.site.register(Team)
