from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Stock, StockChange, User, UserProfile
from .serializers import StockSerializer, StockChangeSerializer, UserProfileSerializer
from rest_framework.renderers import JSONRenderer

# This will return a list of stocks
@api_view(["GET"])
def stockList(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    json = JSONRenderer().render(serializer.data)
    return Response(status=status.HTTP_200_OK, data={"data": json})

@api_view(["GET"])
def stock(request, pk):
    stock = Stock.objects.get(pk=pk)
    serializer = StockSerializer(stock)
    json = JSONRenderer().render(serializer.data)
    return Response(status=status.HTTP_200_OK, data={"data": json})

@api_view(["GET"])
def stockChangeList(request):
    stockChanges = StockChange.objects.all()
    serializer = StockChangeSerializer(stockChanges, many=True)
    json = JSONRenderer().render(serializer.data)
    return Response(status=status.HTTP_200_OK, data={"data": json})

@api_view(["GET"])
def stockChange(request, pk):
    stockChange = StockChange.objects.get(pk=pk)
    serializer = StockChangeSerializer(stockChange)
    json = JSONRenderer().render(serializer.data)
    return Response(status=status.HTTP_200_OK, data={"data": json})

@api_view(["GET"])
def user(request, pk):
    user = UserProfile.objects.get(pk=pk)
    serializer = UserProfileSerializer(user)
    json = JSONRenderer().render(serializer.data)
    return Response(status=status.HTTP_200_OK, data={"data": json})


