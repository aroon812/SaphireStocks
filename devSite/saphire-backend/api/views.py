from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Stock
from .serializers import StockSerializer
from rest_framework.renderers import JSONRenderer

# This will return a list of stocks
@api_view(["GET"])
def stocks(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    print(serializer.data)
    json = JSONRenderer().render(serializer.data)
    print(json)
    return Response(status=status.HTTP_200_OK, data={"data": json})
