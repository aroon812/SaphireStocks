from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, update_session_auth_hash
from .serializers import UserSerializer
from rest_auth.views import (LoginView, LogoutView, PasswordChangeView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import json

class UserList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, status.HTTP_200_OK)

    def post(self, request, format='json'):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        try:
            user = get_user_model().objects.get(pk=pk)
            serializer = UserSerializer(user)
            json_str = json.dumps(serializer.data, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, 404)


    def put(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        update_session_auth_hash(request, user)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        try:
            user = get_user_model().objects.get(pk=pk)
            user.delete()
            return Response({}, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_404_NOT_FOUND)

class CurrentUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, format=None):
        try:
            user = request.user
            serializer = UserSerializer(user)
            json_str = json.dumps(serializer.data, ensure_ascii=False)
            loadedJson = json.loads(json_str)
            return Response(loadedJson, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, 404)

class APILogoutView(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class APILoginView(LoginView):
    pass

class APIPasswordUpdateView(PasswordChangeView):
    authentication_classes = [TokenAuthentication]
