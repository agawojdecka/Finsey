from django.urls import path

from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    GetBalanceView
)

urlpatterns = [
    path("", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-list-create"),
    path("balance/", GetBalanceView.as_view(), name="balance-detail"),
]
