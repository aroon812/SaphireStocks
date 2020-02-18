from rest_framework import serializers
from .models import User, Stock, UserProfile

class StockField(serializers.Field):
    def to_representation(self, obj):
        return obj.pk

    def to_internal_value(self, data):
        return data

class StockSerializer(serializers.ModelSerializer):
    """date = serializers.DateField()
    name = serializers.CharField()
    vol = serializers.IntegerField()
    high = serializers.DecimalField(max_digits=4, decimal_places=2)
    low = serializers.DecimalField(max_digits=4, decimal_places=2)
    avg = serializers.DecimalField(max_digits=4, decimal_places=2)
    open = serializers.DecimalField(max_digits=4, decimal_places=2)
    close = serializers.DecimalField(max_digits=4, decimal_places=2)"""
    class Meta:
        model = Stock
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    watchedStocks = StockSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'

class StockChangeSerializer(serializers.Serializer):
    stock = StockField()
    date = serializers.DateField()
    vol = serializers.IntegerField()
    high = serializers.DecimalField(max_digits=4, decimal_places=2)
    low = serializers.DecimalField(max_digits=4, decimal_places=2)
    avg = serializers.DecimalField(max_digits=4, decimal_places=2)
    open = serializers.DecimalField(max_digits=4, decimal_places=2)
    close = serializers.DecimalField(max_digits=4, decimal_places=2)



