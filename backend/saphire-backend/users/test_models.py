from django.test import TestCase
#from .models import MyUserManager
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    """Test module for User model"""

    def setUp(self):
        get_user_model().objects._create_user(username="test@test.com", email="test@test.com", password="testPassword")
    
    def test_user_email(self):
        testuser = get_user_model().objects.get(email="test@test.com")
        self.assertEqual(
            testuser.email, "test@test.com"
        )

