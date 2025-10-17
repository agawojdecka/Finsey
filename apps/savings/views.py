import dataclasses

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.savings.filters import SavingFilter
from apps.savings.models import Goal, Saving
from apps.savings.serializers import (
    GoalProgressByMonthlySavingsSerializer,
    GoalProgressPercentageSerializer,
    GoalSerializer,
    SavingSerializer,
)
from apps.savings.services.goal_progess import (
    calculate_goal_progress_by_monthly_savings,
    calculate_goal_progress_percentage,
)


class SavingModelViewSet(ModelViewSet):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SavingFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Saving.objects.filter(user=self.request.user)

    def perform_create(self, serializer: SavingSerializer) -> None:
        serializer.save(user=self.request.user)


class GoalModelViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GoalSerializer) -> None:
        serializer.save(user=self.request.user)


class GoalProgressByMonthlySavingsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = GoalProgressByMonthlySavingsSerializer(data=request.data)
        if serializer.is_valid():
            monthly_savings = serializer.validated_data['monthly_savings']
            goal_id = serializer.validated_data['goal_id']
            user = request.user

            try:
                goal = Goal.objects.get(id=goal_id, user=user)
            except Goal.DoesNotExist:
                return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)

            goal_progress = calculate_goal_progress_by_monthly_savings(goal, monthly_savings)
            goal_progress_dict = dataclasses.asdict(goal_progress)
            return Response(goal_progress_dict)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalProgressPercentageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = GoalProgressPercentageSerializer(data=request.data)
        if serializer.is_valid():
            goal_id = serializer.validated_data['goal_id']
            user = request.user

            try:
                goal = Goal.objects.get(id=goal_id, user=user)
            except Goal.DoesNotExist:
                return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)

            goal_progress = calculate_goal_progress_percentage(goal)
            goal_progress_dict = dataclasses.asdict(goal_progress)
            return Response(goal_progress_dict)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
