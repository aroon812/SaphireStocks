from rest_framework import serializers
from .models import User, Stock, StockChange, Company
from django.contrib.auth import get_user_model
from .stockUtils import fillStockFields, normalize_stock

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

    def create(self, validated_data):
        stock = Stock.objects.create(
            company=validated_data['company'],
            date=validated_data['date'],
            vol=validated_data['vol'],
            high=validated_data['high'],
            low=validated_data['low'],
            open=validated_data['open'],
            close=validated_data['close']
        )
        stock.save()
        newStock = Stock.objects.get(date=stock.date, company=stock.company) 
        fillStockFields(newStock, newStock.company)
        normalize_stock(newStock)
        return stock
    
    class Meta:
        model = Stock
        fields = '__all__'

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



