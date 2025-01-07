from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import TransactionFilter
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )  # Return transactions for the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )  # Return transactions for the logged-in user


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )  # Return categories for the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )  # Return categories for the logged-in user


class GetBalanceView(APIView):
    """
    API view to calculate and retrieve the balance (INCOME - EXPENSE).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        incomes = transactions.filter(transaction_type=Transaction.Types.INCOME).aggregate(total=Sum('amount'))[
                      'total'] or 0
        expenses = transactions.filter(transaction_type=Transaction.Types.EXPENSE).aggregate(total=Sum('amount'))[
                       'total'] or 0

        balance = incomes - expenses

        return Response({
            "incomes": incomes,
            "expenses": expenses,
            "balance": balance
        })
