from django.db.models import QuerySet
from rest_framework import permissions, viewsets

from .models import Document
from .serializers import DocumentSerializer


class DocumentModelViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer: DocumentSerializer) -> None:
        serializer.save(user=self.request.user)
