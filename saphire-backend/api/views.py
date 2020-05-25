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
from datetime import datetime, timedelta
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from .utils import update_historical_stocks, current_day_info, update_stock
import json
from machineLearning.predict import predictStock
from django.db.models import Q, Max

class StockList(APIView):
    def get(self, request, format=None):
        stocks = SaphireStock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

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
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

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
        try:
            company = SaphireCompany.objects.get(pk=pk)
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                json_str = json.dumps(serializer.data, ensure_ascii=False)
                loadedJson = json.loads(json_str)
                return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

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

    def delete(self, request, pk, format="json"):
        data = request.data
        symbol=data.get('symbol')
        try:
            company = SaphireCompany.objects.get(symbol=symbol)
            company.delete()
            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

class Stock(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk, format=None):
        stock = SaphireStock.objects.get(pk=pk)
        serializer = StockSerializer(stock)
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

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

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def stock_range(request, format="json"):
    if request.method == 'POST':
        ticker = request.data.get("ticker")
        low_date = request.data.get("low_date")
        high_date = request.data.get("high_date")
        try:
            stock_days = SaphireStock.objects.filter(company=ticker, date__range=[low_date, high_date]).values()
            stock_dict = {}
            day_list = []
            
            for day in stock_days.iterator():
                day_list.append({
                        'date': str(day['date']),
                        'open': float(day['open']),
                        'close': float(day['close']),
                        'high': float(day['high']),
                        'low': float(day['low']),
                        'vol': day['vol'] 
                })
            
            json_str = json.dumps(day_list, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

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
            user = get_user_model().objects._create_user(email=data.get("email"), password=data.get("password"), username=data.get("email"), first_name=data.get("first_name"), last_name=data.get("last_name"))
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        symbol = data.get("symbol")

        try:
            user = request.user
            stock = SaphireCompany.objects.get(symbol=symbol)
            user.watchedStocks.add(stock)
            user.save()
            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

    def delete(self, request, format=None):
        data = request.data
        symbol = data.get("symbol")

        try:
            user = request.user
            stock = SaphireCompany.objects.get(symbol=symbol)
            user.watchedStocks.remove(stock)
            user.save()
            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

class UpdateStock(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format='json'): 
        try:  
            update_historical_stocks()     
            return Response({}, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)
    
class GetWatchedStocks(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            watched_companies = request.user.watchedStocks
            company_dict = {}
            today = datetime.strptime(str(datetime.date(datetime.today())), '%Y-%m-%d')
            prev_date = today - timedelta(days=30)
            for company in watched_companies.all():
                stock_days = SaphireStock.objects.filter(company=company, date__range=[prev_date, today])
                day_list = []
                for day in stock_days:
                    serializer = StockSerializer(day)
                    day_list.append(serializer.data)
                company_dict[company.name] = day_list
            
            json_str = json.dumps(company_dict, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, 200)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

class DeleteStockList(APIView):
    """
    Test endpoint. Not for production.
    """
    def delete(self, request):
        data = request.data  
        try:
            stocks = SaphireStock.objects.filter(company="XOM")
            stocks.delete()
            return Response({}, 200)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def predict(request, format="json"):
    if request.method == 'POST':
        ticker = request.data.get("ticker")
        date = request.data.get("date")
        try: 
            key = '23V86RX6LO5AUIX4'
            ts = TimeSeries(key)
            stocks = SaphireStock.objects.filter(company=ticker)
            stock, meta = ts.get_intraday(symbol=ticker, interval='1min')
            recent = list(stock)[0]
            
            recent_date = stocks.aggregate(Max('date'))
            date_str = recent_date['date__max']
            close = float(stock[recent]['4. close'])

            stocks = SaphireStock.objects.filter(company=ticker)
            date_str = recent_date['date__max']
            prev_stock = SaphireStock.objects.get(company=ticker, date=date_str)
            predictions = predictStock(ticker, date)
            percentage_change = predictions[0] 
            projected_price = (percentage_change+1)*float(prev_stock.close)
            if percentage_change < 0:
                directional_prediction = '-'
            else:
                directional_prediction = '+'

            if predictions[1][0] == 0:
                five_day_boom = 'False'
            else:
                five_day_boom = 'True'
            
            five_day_boom_confidence = predictions[1][1]
            print(percentage_change)
            predict_dict = {
                'last_day_close': float(prev_stock.close),
                'current_price': close,
                'percentage_change': percentage_change*100,
                'projected_price': projected_price,
                'directional_prediction': directional_prediction,
                'five_day_boom': five_day_boom,
                'five_day_boom_confidence': five_day_boom_confidence
            }

            json_str = json.dumps(predict_dict, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def search(request, format="json"):
    if request.method == 'POST':     
        query = request.data.get("query")
        
        try:
            company = SaphireCompany.objects.get(Q(name=query) | Q(symbol=query))
            serializer = CompanySerializer(company)
            
            json_str = json.dumps(serializer.data, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def recent_stock_info(request, format="json"):
    if request.method == 'POST':     
        ticker = request.data.get("ticker")
        try:
            recent_info = current_day_info(ticker)
            json_str = json.dumps(recent_info, ensure_ascii=False)
            loadedJson = json.loads(json_str)

            return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def delete_duplicates(request, format="json"):
    """
    Test endpoint. Not for production.
    """
    if request.method == 'POST':     
        try:
            for row in SaphireStock.objects.all():
                print(row)
                if SaphireStock.objects.filter(company=row.company, date=row.date).count() > 1:
                    row.delete()
                    print("duplicate deleted")

            return Response(loadedJson, 200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, 400)
