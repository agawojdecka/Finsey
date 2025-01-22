from django.urls import path
from rest_framework import routers

from .views import TransactionModelViewSet, CategoryModelViewSet, GetBalanceView, GetReportView, \
    GetMonthlyExpenseReportView

router = routers.SimpleRouter()
router.register('categories', CategoryModelViewSet)
router.register('', TransactionModelViewSet)

urlpatterns = [
                  path("balance/", GetBalanceView.as_view(), name="balance-detail"),
                  path("report/", GetReportView.as_view(), name="report-detail"),
                  path("monthly-expense-report/", GetMonthlyExpenseReportView.as_view(),
                       name="monthly-expense-report-detail"),
              ] + router.urls
