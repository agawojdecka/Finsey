from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer


class DocumentModelViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return documents belonging to the authenticated user
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the document to the logged-in user
        serializer.save(user=self.request.user)
