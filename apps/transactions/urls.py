from django.urls import path
from rest_framework import routers

from .views import TransactionModelViewSet, CategoryModelViewSet, GetBalanceView

router = routers.SimpleRouter()
router.register('categories', CategoryModelViewSet)
router.register('', TransactionModelViewSet)

urlpatterns = [
                  path("balance/", GetBalanceView.as_view(), name="balance-detail"),
              ] + router.urls
