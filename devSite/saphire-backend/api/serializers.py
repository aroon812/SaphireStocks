from rest_framework import serializers

class StockSerializer(serializers.Serializer):
    date = serializers.DateField()
    name = serializers.CharField()
    vol = serializers.IntegerField()
    high = serializers.DecimalField(max_digits=4, decimal_places=2)
    low = serializers.DecimalField(max_digits=4, decimal_places=2)
    avg = serializers.DecimalField(max_digits=4, decimal_places=2)
    open = serializers.DecimalField(max_digits=4, decimal_places=2)
    close = serializers.DecimalField(max_digits=4, decimal_places=2)