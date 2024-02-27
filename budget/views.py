from django.shortcuts import render
from rest_framework.views import APIView
from budget.serializers import UserSerializer,TransactionSerializer,TransactionSummarySerializer
from rest_framework.response import Response
from rest_framework import viewsets
from budget.models import Transaction
from django .utils import timezone
from rest_framework import authentication,permissions
from django.db.models import Sum

class SignUpView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class TransactionsView(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()
    cur_month=timezone.now().month
    cur_year=timezone.now().year

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return Transaction.objects.filter(
                                            user=self.request.user,
                                          created_date__month=self.cur_month,
                                          created_date__year=self.cur_year
                                          )
class TransactionSummaryAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]
    cur_month=timezone.now().month
    cur_year=timezone.now().year

    def get(self, request,*args,**kwargs):

        transactions = Transaction.objects.filter(user=request.user,
                                                  created_date__month=self.cur_month,
                                                  created_date__year=self.cur_year
                                                  )
        
        total_expense = transactions.filter(type='expenses').aggregate(total_expense=Sum('amount'))['total_expense'] or 0
        total_income = transactions.filter(type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
        
        category_summary = transactions.values('category').annotate(total_amount=Sum('amount')).order_by('category')
        category_summary = {category['category']: category['total_amount'] for category in category_summary}
        
        data = {
            'total_expense': total_expense,
            'total_income': total_income,
            'category_summary': category_summary
        }
        
        serializer = TransactionSummarySerializer(data)
        return Response(serializer.data)