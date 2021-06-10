from rest_framework import serializers
from .models import Stock, Company
from .stockUtils import fillStockFields


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
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all())

    def create(self, validated_data):
        if Stock.objects.filter(date=validated_data['date'], company=validated_data['company']).exists():
            raise Exception("stock already exists")
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
        return stock

    class Meta:
        model = Stock
        fields = '__all__'
