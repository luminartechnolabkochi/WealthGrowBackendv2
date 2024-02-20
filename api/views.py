from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers import TransactionSerializer
from api.models import Transaction

# Create your views here.


class TransactionView(viewsets.ModelViewSet):
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()