import json 
from rest_framework import status
from rest_framework.authtoken.models import Token
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


class GetSingleUserTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects._create_user(username="test1@test.com" ,email="test1@test.com", password="testPassword1")
        self.user2 = get_user_model().objects._create_user(username="test2@test.com" ,email="test2@test.com", password="testPassword2")
        self.user3 = get_user_model().objects._create_user(username="test3@test.com" ,email="test3@test.com", password="testPassword3")
        self.user4 = get_user_model().objects._create_user(username="test4@test.com" ,email="test4@test.com", password="testPassword4")
    
    def test_get_valid_single_user(self):
        response = client.get(reverse("user", kwargs={"pk": self.user1.pk}))
        user = get_user_model().objects.get(pk=self.user1.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_single_user(self):
        response = client.get(reverse("user", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleUserTestCase(TestCase):

    def setUp(self):
        self.valid_payload = {
            'email': 'testemail1@test.com',
            'password': 'testPassword1'
        }
        self.invalid_payload = {
            'email': 'testemail2@test.com'
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('userList'), 
            data=json.dumps(self.valid_payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse('userList'), 
            data=json.dumps(self.invalid_payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects._create_user(username="test1@test.com" ,email="test1@test.com", password="testPassword1")
        self.valid_payload = {
            'email': 'newemail@test.com',
            'password': 'testPassword1'
        }
        self.invalid_payload = {
            'email': 'testemail2@test.com'
        }

    def test_update_valid_user(self):
        response = client.put(
            reverse('user', kwargs={"pk": self.user1.pk}), 
            data=json.dumps(self.valid_payload), 
            content_type='application/json'
        )
        user = get_user_model().objects.get(pk=self.user1.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.valid_payload["email"], user.email)

    def test_update_invalid_user(self):
        response = client.put(
            reverse('user', kwargs={"pk": self.user1.pk}), 
            data=json.dumps(self.invalid_payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects._create_user(username="test1@test.com" ,email="test1@test.com", password="testPassword1")

    def test_valid_delete_user(self):
        response = client.delete(
            reverse('user', kwargs={"pk": self.user1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_user(self):
        response = client.delete(
            reverse('user', kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetCurrentUser(TestCase):
    def setUp(self):
        email = "test1@test.com"
        password = "testPassword1"
        self.current_user = get_user_model().objects._create_user(username=email,email=email, password=password)
        credentials = {
            "username":email, 
            "password":password
        }
        self.signin_response = client.post(
                                reverse("api_login"), 
                                data=json.dumps(credentials),
                                content_type='application/json')

        
    def test_get_valid_current_user(self):
        headers = {"HTTP_AUTHORIZATION": "Token " + self.signin_response.data["key"]}
        response = client.get(reverse("current_user"), **headers)
        user = get_user_model().objects.get(email=self.current_user.email)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_current_user(self):
        headers = {"HTTP_AUTHORIZATION": "Token badToken"}
        response = client.get(reverse("current_user"), **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateCurrentUser(TestCase):
    def setUp(self):

        email = "test1@test.com"
        password = "testPassword1"
        self.current_user = get_user_model().objects._create_user(username=email,email=email, password=password)
        credentials = {
            "username":email, 
            "password":password
        }
        self.signin_response = client.post(
                                reverse("api_login"), 
                                data=json.dumps(credentials),
                                content_type='application/json')
        self.valid_payload = {
            'email': 'newemail@test.com',
            'password': 'testPassword1'
        }
        self.invalid_payload = {
            'email': 'testemail2@test.com'
        }

        
    def test_update_valid_current_user(self):

        headers = {"HTTP_AUTHORIZATION": "Token " + self.signin_response.data["key"]}
        response = client.put(
                    reverse("current_user"), 
                    data=json.dumps(self.valid_payload), 
                    content_type='application/json',
                    **headers)
        user = Token.objects.get(key=self.signin_response.data["key"]).user

        self.assertEqual(self.valid_payload["email"], user.email)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_update_invalid_current_user(self):

        headers = {"HTTP_AUTHORIZATION": "Token " + self.signin_response.data["key"]}
        response = client.put(
                    reverse("current_user"), 
                    data=self.invalid_payload, 
                    content_type='application/json', 
                    **headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateCurrentUserPartial(TestCase):
    def setUp(self):

        email = "test1@test.com"
        password = "testPassword1"
        self.current_user = get_user_model().objects._create_user(username=email,email=email, password=password)
        credentials = {
            "username":email, 
            "password":password
        }
        self.signin_response = client.post(
                                reverse("api_login"), 
                                data=json.dumps(credentials),
                                content_type='application/json')
        self.valid_payload = {
            'email': 'newemail@test.com',
        }
    
        
    def test_update_valid_current_user_partial(self):

        headers = {"HTTP_AUTHORIZATION": "Token " + self.signin_response.data["key"]}
        user = Token.objects.get(key=self.signin_response.data["key"]).user
        response = client.patch(
                    reverse("current_user"), 
                    data=json.dumps(self.valid_payload), 
                    content_type='application/json',
                    **headers)
        user = Token.objects.get(key=self.signin_response.data["key"]).user

        self.assertEqual(self.valid_payload["email"], user.email)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
