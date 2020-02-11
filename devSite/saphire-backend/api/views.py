from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# This will return a list of stocks
@api_view(["GET"])
def stocks(request):
    stocks = ["BigTuba", "Spookaliah", "olob", "the grand master"]
    return Response(status=status.HTTP_200_OK, data={"data": stocks})
