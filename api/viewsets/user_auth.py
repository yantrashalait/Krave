from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.db import transaction
from django.contrib.auth.models import Group
from api.serializers.user_auth import UserProfileSerializer, UserSerializer
from userrole.models import UserRole
from user.models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from api.permissions import IsOwnerOrReadOnly, IsOwner


class CustomAuthToken(ObtainAuthToken):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=False)
        try:
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': True,
                'msg': 'Login Successful',
                'data': {
                    'token': token.key,
                    'user_id': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'restaurant': user.is_restaurant,
                    'customer': user.is_customer,
                    'delivery': user.is_deliveryman,
                }

            }, status=status.HTTP_200_OK)
        except KeyError:
            return Response({
                'status': False,
                'msg': 'Login Failed',
            }, status=status.HTTP_400_BAD_REQUEST)


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
                return Response(
                    {
                        'status': True,
                        'msg': 'Registration successful.',
                    }, status=status.HTTP_200_OK
                )
        else:
            return Response({
                'status': False,
                'msg': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = UserProfileSerializer

    def get_object(self, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        self.check_object_permissions(self.request, profile)
        return profile

    # create user profile of user
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['user'] = self.request.user
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Created successfully.'
        }, status=status.HTTP_200_OK)

    # update user profile of user
    def put(self, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Updated successfully.'
        }, status=status.HTTP_200_OK)

    # get user profile of user
    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)



