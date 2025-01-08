from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.savings.filters import SavingFilter
from apps.savings.models import Saving, Goal
from apps.savings.serializers import SavingSerializer, GoalSerializer


class SavingModelViewSet(ModelViewSet):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = SavingFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Saving.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalModelViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
