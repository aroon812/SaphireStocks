import json 
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse 
from .models import User 
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

client = Client()

class GetAllUsersTest(TestCase):
    def setUp(self):
        get_user_model().objects._create_user(username="test1@test.com" ,email="test1@test.com", password="testPassword1")
        get_user_model().objects._create_user(username="test2@test.com" ,email="test2@test.com", password="testPassword2")
        get_user_model().objects._create_user(username="test3@test.com" ,email="test3@test.com", password="testPassword3")
        get_user_model().objects._create_user(username="test4@test.com" ,email="test4@test.com", password="testPassword4")

    def test_get_all_users(self):
        response = client.get(reverse('userList'))
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)