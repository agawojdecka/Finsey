from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.transactions.services.balance import get_balance
from apps.transactions.tasks import generate_and_send_report_task, generate_monthly_expense_report_task
from apps.transactions.filters import TransactionFilter
from apps.transactions.models import Transaction, Category
from apps.transactions.serializers import TransactionSerializer, CategorySerializer, ColumnsListSerializer, TransactionToSavingSerializer


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
            generate_and_send_report_task.delay(user_id=self.request.user.id, selected_columns=selected_columns)

            return Response({'message': "Report has been sent."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMonthlyExpenseReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        generate_monthly_expense_report_task.delay(user_id=self.request.user.id)
        return Response({'message': "Monthly expense report has been generated."})


class TransactionToSavingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': "Saving has been added."})


        # serializer = TransactionToSavingSerializer(data=request.data)
        # if serializer.is_valid():
        #     saving = Saving.objects.create(operation_type="INFLOW", amount=serializer.validated_data['amount'], user=self.request.user)
        #     saving.save()
        #     return Response({'message': "Saving has been added."})