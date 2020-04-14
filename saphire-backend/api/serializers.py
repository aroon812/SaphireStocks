from rest_framework import serializers
from .models import User, Stock, StockChange, Company
from django.contrib.auth import get_user_model

class StockField(serializers.Field):
    def to_representation(self, obj):
        return obj.pk

    def to_internal_value(self, data):
        return data

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Stock
        fields = ['id', 'company', 'date', 'vol', 'high', 'low', 'avg', 'open', 'close']

class UserSerializer(serializers.ModelSerializer):
    watchedStocks = CompanySerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = '__all__'

class StockChangeSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())

    class Meta:
        model = StockChange
        fields = '__all__'



