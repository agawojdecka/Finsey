from django.urls import path

from .views import (
    SavingListCreateView,
    SavingDetailView,
    GoalListCreateView,
    GoalDetailView,
)

urlpatterns = [
    path("", SavingListCreateView.as_view(), name="saving-list-create"),
    path("<int:pk>/", SavingDetailView.as_view(), name="saving-detail"),
    path("goals/", GoalListCreateView.as_view(), name="goal-list-create"),
    path("goals/<int:pk>/", GoalDetailView.as_view(), name="goal-detail"),
]
