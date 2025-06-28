from django.db import models
from django.conf import settings

class ToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_approve_todo", "Can approve a todo"),
            ("can_edit_others_todo", "Can edit todos of other users"),
            ("can_delete_others_todo", "Can delete todos of other users"),
        ]

    def __str__(self):
        return self.title
