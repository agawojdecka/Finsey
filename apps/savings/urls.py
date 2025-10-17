from django.urls import path
from rest_framework import routers

from apps.savings.views import (
    GoalModelViewSet,
    GoalProgressByMonthlySavingsView,
    GoalProgressPercentageView,
    SavingModelViewSet,
)

router = routers.SimpleRouter()
router.register('goals', GoalModelViewSet)
router.register('', SavingModelViewSet)

urlpatterns = [
    path(
        'goals/progress_by_monthly_savings/',
        GoalProgressByMonthlySavingsView.as_view(),
        name='goal-progress-by-monthly-savings',
    ),
    path('goals/percentage_progress/', GoalProgressPercentageView.as_view(), name='goal-percentage-progress'),
] + router.urls
