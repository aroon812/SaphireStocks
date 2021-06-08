from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Stock as SaphireStock, Company as SaphireCompany
from .serializers import StockSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from .utils import current_day_info
import json
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication

class StockList(APIView):
    def get(self, request, format=None):
        stocks = SaphireStock.objects.all()
        print(len(stocks))
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

class CompanyList(APIView):
    def get(self, request, format=None):
        companies = SaphireCompany.objects.all()
        serializer = CompanySerializer(companies, many=True)

        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

    def post(self, request, format='json'):
        data = request.data
        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)


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
            return Response({'error': serializer.errors}, 400)
        except Exception as e:
            return Response({'error': str(e)}, 400)

    def put(self, request, pk, format="json"):
        company = SaphireCompany.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)

    def patch(self, request, pk, format="json"):
        company = SaphireCompany.objects.get(pk=pk)
        serializer = CompanySerializer(
            company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)

    def delete(self, request, pk, format="json"):
        data = request.data
        symbol = data.get('symbol')
        try:
            company = SaphireCompany.objects.get(symbol=symbol)
            company.delete()
            return Response({}, 200)
        except Exception as e:
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
        return Response({'error': serializer.errors}, 400)

    def patch(self, request, pk, format="json"):
        stock = SaphireStock.objects.get(pk=pk)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)

    def delete(self, request, pk, format=None):
        try:
            stock = SaphireStock.objects.get(pk=pk)
            stock.delete()
            return Response({}, 204)
        except Exception as e:
            return Response({'error': str(e)}, 400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def stock_range(request, format="json"):
    if request.method == 'POST':
        ticker = request.data.get("ticker")
        low_date = request.data.get("low_date")
        high_date = request.data.get("high_date")
        try:
            stock_days = SaphireStock.objects.filter(company=ticker, date__range=[
                                                     low_date, high_date]).values()
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

class WatchStock(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
            return Response({'error': str(e)}, 400)


class GetWatchedStocks(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            watched_companies = request.user.watchedStocks
            company_dict = {}
            today = datetime.strptime(
                str(datetime.date(datetime.today())), '%Y-%m-%d')
            prev_date = today - timedelta(days=30)
            for company in watched_companies.all():
                stock_days = SaphireStock.objects.filter(
                    company=company, date__range=[prev_date, today])
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
            

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def search(request, format="json"):
    if request.method == 'POST':
        query = request.data.get("query")

        try:
            company = SaphireCompany.objects.get(
                Q(name=query) | Q(symbol=query))
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
