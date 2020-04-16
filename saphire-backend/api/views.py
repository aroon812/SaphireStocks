from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Stock as SaphireStock, StockChange as SaphireStockChange, Company as SaphireCompany
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .serializers import StockSerializer, StockChangeSerializer, UserSerializer, CompanySerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from rest_framework.decorators import api_view


class StockList(APIView):

    def get(self, request, format=None):
        stocks = SaphireStock.objects.all()
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

class StockChangeList(APIView):

    def get(self, request, format=None):
        stock_changes = SaphireStockChange.objects.all()
        serializer = StockChangeSerializer(stock_changes, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = request.data
        serializer = StockChangeSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({}, 400)

class CompanyList(APIView):

    def get(self, request, format=None):
        companies = SaphireCompany.objects.all()
        serializer = CompanySerializer(companies, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):
        data = request.data
        serializer = CompanySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class Company(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        company = SaphireCompany.objects.get(pk=pk)
        serializer = CompanySerializer(company)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def put(self, request, pk, format="json"):
        company = SaphireCompany.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        company = SaphireCompany.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

class Stock(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stock = SaphireStock.objects.get(pk=pk)
        serializer = StockSerializer(stock)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def put(self, request, pk, format="json"):
        stock = SaphireStock.objects.get(pk=pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        stock = SaphireStock.objects.get(pk=pk)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def delete(self, request, pk, format=None):
        stock = SaphireStock.objects.get(pk=pk)
        stock.delete()
        return Response({}, 204)

class StockChange(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stock_change = SaphireStockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stock_change)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json}) 

    def put(self, request, pk, format="json"):
        stock_change = SaphireStockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stock_change, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        stock_change = SaphireStockChange.objects.get(pk=pk)
        serializer = StockChangeSerializer(stock_change, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def delete(self, request, pk, format=None):
        stock_change = SaphireStockChange.objects.get(pk=pk)
        stock_change.delete()
        return Response({}, 204)

class UserList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def post(self, request, format='json'):

        data = request.data
        if not get_user_model().objects.filter(email=data.get("email")).exists():
            user = get_user_model().objects._create_user(email=data.get("email"), password=data.get("password"), username=data.get("username"))
            if user is not None:
                user.save()
                return Response({}, 200)
            else:
                return Response({}, 400)
        else:
            return Response({'message': 'The provided email address is already in use.'}, 409)
        
class User(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user)
        json = JSONRenderer().render(serializer.data)
        return Response(status=status.HTTP_200_OK, data={"data": json})

    def put(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        update_session_auth_hash(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        print(serializer.errors)
        return Response({}, 400)

    def patch(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        print(type(request.data))
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

@api_view(['POST'])
def change_password(request, pk, format="json"):
    if request.method == 'POST':
        password = request.data.get("password")
        try:
            user = get_user_model().objects.get(pk=pk)
            user.set_password(password)
            user.save()
            return Response({}, 200)
        except:
            return Response({}, 400)

class WatchStock(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        user_id = data.get("userID")
        symbol = data.get("symbol")

        try:
            user = get_user_model().objects.get(pk=user_id)
            stock = SaphireCompany.objects.get(symbol=symbol)

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
            recent_date = list(stock)[0]
            stock_dict = dict(stock[recent_date])
            
            stock = SaphireStock.objects.create(date=recent_date, company=symbol, open=stock_dict['1. open'], high=stock_dict['2. high'], low=stock_dict['3. low'], close=stock_dict['4. close'], vol=stock_dict['5. volume'], avg=0)
            stock.save()

            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)
    
class Signin(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (AllowAny,)

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




