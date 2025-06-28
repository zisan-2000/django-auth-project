from django.urls import path
from .views import ToDoListCreateView, ToDoDetailView, ApproveToDoView

urlpatterns = [
    path('', ToDoListCreateView.as_view(), name='todo-list-create'),
    path('<int:pk>/', ToDoDetailView.as_view(), name='todo-detail'),
    path('<int:pk>/approve/', ApproveToDoView.as_view(), name='todo-approve'),  # ✅ NEW
]
