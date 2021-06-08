from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, update_session_auth_hash
from .serializers import UserSerializer
from rest_auth.views import (LoginView, LogoutView, PasswordChangeView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

class UserList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

    def post(self, request, format='json'):
        data = request.data

        if not get_user_model().objects.filter(email=data.get("email")).exists():
            user = get_user_model().objects._create_user(email=data.get("email"), password=data.get("password"),
                                                         username=data.get("email"), first_name=data.get("first_name"), last_name=data.get("last_name"))
            if user is not None:
                user.save()
                return Response({}, 200)
            else:
                return Response({'error': 'User was not saved.'}, 400)
        else:
            return Response({'message': 'The provided email address is already in use.'}, 409)


class User(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user)
        json_str = json.dumps(serializer.data, ensure_ascii=False)
        loadedJson = json.loads(json_str)
        return Response(loadedJson, 200)

    def put(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        update_session_auth_hash(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)

    def patch(self, request, pk, format="json"):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response({'error': serializer.errors}, 400)

    def delete(self, request, pk, format=None):
        try:
            user = get_user_model().objects.get(pk=pk)
            user.delete()
            return Response({}, 204)
        except Exception as e:
            return Response({'error': str(e)}, 400)


class APILogoutView(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class APILoginView(LoginView):
    pass

class APIPasswordUpdateView(PasswordChangeView):
    authentication_classes = [TokenAuthentication]
