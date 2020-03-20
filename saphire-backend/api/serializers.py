from rest_framework import serializers
from .models import User, Stock, StockChange
from django.contrib.auth import get_user_model

class StockField(serializers.Field):
    def to_representation(self, obj):
        return obj.pk

    def to_internal_value(self, data):
        return data

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id','symbol','date', 'name', 'vol', 'high', 'low', 'avg', 'open', 'close']

class UserSerializer(serializers.ModelSerializer):
    watchedStocks = StockSerializer(many=True, read_only=True)

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



