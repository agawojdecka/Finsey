from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.transactions.services.balance import get_balance
from apps.transactions.tasks import create_report
from .filters import TransactionFilter
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer, ColumnsListSerializer


class TransactionModelViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        balance_dict = get_balance(request.user)

        return Response(balance_dict)


class GetReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ColumnsListSerializer(data=request.data)
        if serializer.is_valid():
            selected_columns = serializer.validated_data['selected_columns']
            create_report.delay(user_id=self.request.user.id, selected_columns=selected_columns)

            return Response({'message': "Task submitted"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
