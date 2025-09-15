from typing import Any, cast

from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "title",
            "document_type",
            "uploaded_at",
            "note",
            "user",
            "file",
        ]
        read_only_fields = ["id", "uploaded_at", "user"]

    def create(self, validated_data: dict[str, Any]) -> Document:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return cast(Document, super().create(validated_data))
