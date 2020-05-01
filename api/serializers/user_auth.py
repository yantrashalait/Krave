from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from user.models import UserProfile



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=500, required=True)
    username = serializers.CharField(max_length=500, required=True)
    password = serializers.CharField(min_length=8)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        return user

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("User with this username already exists.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return email

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = '__all__'
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        UserProfile.objects.create(user=user, **validated_data)
        return super(UserProfileSerializer, self).create(validated_data)
