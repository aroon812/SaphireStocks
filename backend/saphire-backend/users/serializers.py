from api.serializers import CompanySerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

class UserSerializer(serializers.ModelSerializer):
    watchedStocks = CompanySerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'watchedStocks']
