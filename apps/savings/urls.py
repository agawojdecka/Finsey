from django.urls import path
from rest_framework import routers

from apps.savings.views import SavingModelViewSet, GoalModelViewSet, GoalProgressView

router = routers.SimpleRouter()
router.register('goals', GoalModelViewSet)
router.register('', SavingModelViewSet)

urlpatterns = [
                  path('goals/progress/', GoalProgressView.as_view(), name='goal-progress')
              ] + router.urls
