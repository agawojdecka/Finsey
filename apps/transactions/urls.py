from django.urls import path
from rest_framework import routers

from .views import (
    CategoryModelViewSet,
    GetBalanceView,
    GetMonthlyExpenseReportView,
    GetReportView,
    PlannedTransactionViewSet,
    TransactionModelViewSet,
    TransactionToSavingView,
)

router = routers.SimpleRouter()
router.register('categories', CategoryModelViewSet, basename='categories')
router.register('plan', PlannedTransactionViewSet, basename='planned_transactions')
router.register('', TransactionModelViewSet, basename='transactions')

urlpatterns = [
    path("balance/", GetBalanceView.as_view(), name="balance-detail"),
    path("report/", GetReportView.as_view(), name="report-detail"),
    path(
        "monthly-expense-report/",
        GetMonthlyExpenseReportView.as_view(),
        name="monthly-expense-report-detail",
    ),
    path(
        "transaction-to-saving/",
        TransactionToSavingView.as_view(),
        name="transaction-to-saving-detail",
    ),
] + router.urls
