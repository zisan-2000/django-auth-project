from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]  # 🔐 শুধু logged-in user access পাবে

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # author field auto-assign
