from rest_framework import serializers
from django.contrib.auth.models import User
from budget.models import Transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        read_only_fields=["id"]
        fields=["id","username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TransactionSerializer(serializers.ModelSerializer):


    class Meta:
        model=Transaction
        fields="__all__"
        read_only_fields=["id","created_date","user"]


class TransactionSummarySerializer(serializers.Serializer):
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_summary = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))


    
