from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import User, Company, Rol, Profile


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['name', 'code']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'nit', 'logo']


class RolUserSerializer(serializers.ModelSerializer):
    rol = RolSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ['rol']


class CompanyUserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)
    rol = RolSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ['company', 'rol']


class UserSerializer(serializers.ModelSerializer):
    profile = CompanyUserSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class ProfileSerializer(serializers.ModelSerializer):
    profile = RolUserSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_authenticated_user(self):
        data = self.validated_data
        kwargs = {
            'username': data['login'],
            'password': data['password'],
        }
        user = authenticate(**kwargs)
        return user
