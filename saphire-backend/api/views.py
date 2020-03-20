from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Stock, StockChange
from django.contrib.auth import get_user_model, authenticate, login, logout
from .serializers import StockSerializer, StockChangeSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime


class stockList(APIView):

    def get(self, request, format=None):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = request.data
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
        data = request.data
        serializer = StockChangeSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({}, 400)

class stock(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stock = Stock.objects.get(pk=pk)
        serializer = StockSerializer(stock)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def put(self, request, pk, format="json"):
        stock = Stock.objects.get(pk=pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        stock = Stock.objects.get(pk=pk)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def delete(self, request, pk, format=None):
        stock = Stock.objects.get(pk=pk)
        stock.delete()
        return Response({}, 204)

class stockChange(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stockChange = StockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stockChange)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json}) 

    def put(self, request, pk, format="json"):
        stockChange = StockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stockChange, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        stockChange = StockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stockChange, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def delete(self, request, pk, format=None):
        stockChange = StockChange.objects.get(pk=pk)
        stockChange.delete()
        return Response({}, 204)

class UserList(APIView):
    
    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = request.data
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class User(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def put(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def delete(self, request, pk, format=None):
        user = get_user_model().objects.get(pk=pk)
        user.delete()
        return Response({}, 204)

class WatchStock(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        userID = data.get("userID")
        stockID = data.get("stockID")

        try:
            user = get_user_model().objects.get(pk=userID)
            stock = Stock.objects.get(id=stockID)

            user.watchedStocks.add(stock)
            user.save()

            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

class UpdateStock(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format='json'):
        data = request.data
        #key = 'PLVU0FOZUJ18M46O'
        key = '23V86RX6LO5AUIX4'
        ts = TimeSeries(key)
        
        try:
            print(data)
            symbol = data.get("symbol")
            print("symbol " + str(symbol))
            stock, meta = ts.get_daily(symbol=symbol)
            recentDate = list(stock)[0]
            stockDict = dict(stock[recentDate])
            
            stock = Stock.objects.create(date=recentDate, symbol=symbol, open=stockDict['1. open'], high=stockDict['2. high'], low=stockDict['3. low'], close=stockDict['4. close'], vol=stockDict['5. volume'], avg=0)
            stock.save()

            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)
    
class Signin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print(request.user.is_authenticated)
        print(request.user.username)
        print(request.user.password)

        user = authenticate(username='bash', password='bash')
        print(request.user.is_authenticated)
        print(user)

        if user is not None:
            login(request, user)
            print(request.user.is_authenticated)
            print(user)
            return Response({}, 200)
        else:
            return Response({}, 400)

class Signout(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        print(request.user.is_authenticated)
        logout(request)
        print(request.user.is_authenticated)
        print(request.user)
        return Response({}, 200)

class CheckAuthenticated(APIView):

    def get(self, request, format=None):
        print(request.user)
        authenticated = request.user.is_authenticated

        return Response({authenticated}, 200)




