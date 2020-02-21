from rest_framework import serializers
from .models import User, Stock, UserProfile, StockChange

class StockField(serializers.Field):
    def to_representation(self, obj):
        return obj.pk

    def to_internal_value(self, data):
        return data

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['date', 'name', 'vol', 'high', 'low', 'avg', 'open', 'close']

class UserProfileSerializer(serializers.ModelSerializer):
    watchedStocks = StockSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfile()

    class Meta:
        model = User
        fields = '__all__'

class StockChangeSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())

    class Meta:
        model = StockChange
        fields = '__all__'



