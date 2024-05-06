from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import Account
from core.exceptions import ConflictException, InvalidLogin, PuclicException


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Account
        fields = ["username", "password"]

    def validate(self, data):
        auth = authenticate(username=data["username"], password=data["password"])
        if auth is None:
            raise InvalidLogin({"message": "not valid auth"})
        return data


class SignInResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "username",
            "token",
        ]

    def get_name(self, obj):
        return obj.first_name

    def get_token(self, data):
        refresh = RefreshToken.for_user(data)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
