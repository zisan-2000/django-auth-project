# todo/admin.py

from django.contrib import admin
from .models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)

admin.site.register(ToDo, ToDoAdmin)
