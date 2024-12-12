from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.savings.filters import SavingFilter
from apps.savings.models import Saving, Goal
from apps.savings.serializers import SavingSerializer, GoalSerializer


class SavingListCreateView(generics.ListCreateAPIView):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SavingFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Saving.objects.filter(
            user=self.request.user
        )  # Return savings for the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user


class SavingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Saving.objects.filter(
            user=self.request.user
        )  # Return savings for the logged-in user


class GoalListCreateView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user
        )  # Return goals for the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user
        )  # Return goals for the logged-in user
