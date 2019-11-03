from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import RestaurantSerializer, RestaurantRequestSerializer, UserSerializer, UserProfileSerializer
from core.models import Restaurant, RestaurantRequest
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import Group
from userrole.models import UserRole
from django.db import transaction
from user.models import UserProfile


class CustomAuthToken(ObtainAuthToken):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'restaurant': user.is_restaurant,
            'customer': user.is_customer,
            'delivery': user.is_deliveryman,
        })


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class =  RestaurantSerializer


class RestaurantRequestViewSet(viewsets.ModelViewSet):
    queryset = RestaurantRequest.objects.all()
    serializer_class = RestaurantRequestSerializer


class UserCreationViewSet(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_customer = True
            user.save()
            group = Group.objects.get(name='customer')
            userrole = UserRole.objects.get_or_create(user=user, group=group)
            user.groups.add(group)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    
    def get_queryset(self, pk=None):
        if not pk:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.get(user__id=pk)


