from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.savings.filters import SavingFilter
from apps.savings.models import Saving, Goal
from apps.savings.serializers import SavingSerializer, GoalSerializer, GoalProgressSerializer
from apps.savings.services.goal_progess import calculate_goal_progress


class SavingModelViewSet(ModelViewSet):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SavingFilter
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


class GoalProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GoalProgressSerializer(data=request.data)
        if serializer.is_valid():
            monthly_savings = serializer.validated_data['monthly_savings']
            goal_id = serializer.validated_data['goal_id']
            user = request.user

            try:
                goal = Goal.objects.get(id=goal_id, user=user)
            except Goal.DoesNotExist:
                return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)

            result = calculate_goal_progress(goal, monthly_savings)
            return Response(result)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
