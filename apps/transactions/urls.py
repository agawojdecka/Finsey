from django.urls import path
from rest_framework import routers

from .views import TransactionModelViewSet, CategoryModelViewSet, GetBalanceView, GetReportView, SendEmailView

router = routers.SimpleRouter()
router.register('categories', CategoryModelViewSet)
router.register('', TransactionModelViewSet)

urlpatterns = [
                  path("balance/", GetBalanceView.as_view(), name="balance-detail"),
                  path("report/", GetReportView.as_view(), name="report-detail"),
                  path("email/", SendEmailView.as_view(), name="email-detail"),
              ] + router.urls
