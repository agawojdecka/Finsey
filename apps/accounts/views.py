from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer


class AccountModelViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer: AccountSerializer) -> None:
        serializer.save(user=self.request.user)
