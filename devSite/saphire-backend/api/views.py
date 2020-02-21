from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Stock, StockChange, User, UserProfile
from .serializers import StockSerializer, StockChangeSerializer, UserProfileSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

class stockList(APIView):

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = list(request.data)[0]
        data = json.loads(data)
        print(data)
        serializer = StockSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class stockChangeList(APIView):

    def get(self, request, format=None):
        stockChanges = StockChange.objects.all()
        serializer = StockChangeSerializer(stockChanges, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = list(request.data)[0]
        data = json.loads(data)
        print(data)
        serializer = StockChangeSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class stock(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stock = Stock.objects.get(pk=pk)
        serializer = StockSerializer(stock)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

class stockChange(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        stockChange = StockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stockChange)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json}) 

class UserList(APIView):
    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = list(request.data)[0]
        data = json.loads(data)
        print(data)
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class User(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        user = UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(user)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})
    


