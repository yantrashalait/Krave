import json

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import logout

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes

from api.serializers.user_auth import UserProfileSerializer, UserSerializer
from userrole.models import UserRole
from user.models import UserProfile
from api.permissions import IsOwnerOrReadOnly, IsOwner

from social_django.models import UserSocialAuth
from social_django.utils import psa, load_strategy, load_backend


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


@csrf_exempt
@psa('social:complete')
def exchange_token(request, *args, **kwargs):
    """
        This view handles login and register of user by google.
        This view simply defers the entire OAuth2 process to the fornt end.
        The front end becomes responsible for handling the entirity of the OAuth2 process;
        we just step in at the end and use the access token to populate some user identity.

        The URL at which this view lives must include a backend field, like:
            url(API_ROOT + r'exchange-token/(?P<backend>[^/]+)/$', exchange_token),
        Using that example, you could call this endpoint using i.e.
            POST API_ROOT + 'exchange-token/facebook'
            POST API_ROOT + 'exchange-token/google-oauth2'
            POST API_ROOT + 'exchange-token/apple-id'

        Requests must include the following field:
        - `access_token`: The OAuth2 access token provided by the provider

        The access_token is obtained from the provider in front end and passed in the request data.
    """
    if request.method != "POST":
        out = {
            "ack": False,
            "msg": "Method not allowed",
        }
        return HttpResponse(
            json.dumps(out),
            status=405,
            content_type="application/json"
        )

    # get the access_token from the request data
    request_body = json.loads(request.body)
    access_token = request_body.get("access_token", '')

    # check whether access_token is empty or not
    if not access_token or access_token == "":
        out = {
            "ack": False,
            "msg": "Access token is missing."
        }
        return HttpResponse(
            json.dumps(out),
            status=400,
            content_type="application/json"
        )

    try:
        # this line, plus the psa decorator above, are all that's necessary to
        # get and populate a user object for any properly enabled/configured backend
        # which django-social-auth-app can handle
        user_req = request.backend.do_auth(access_token)
    except Exception as e:
        out = {
            "ack": False,
            "msg": "Authentication failed.",
        }
        return HttpResponse(
            json.dumps(out),
            status=400,
            content_type="application/json"
        )
    if user_req and user_req.is_active:
        try:
            token, _created = Token.objects.get_or_create(user=user_req)

            if not user_req.groups.exists():
                group = Group.objects.get(name="customer")
                user_req.groups.add(group)
                UserRole.objects.get_or_create(user=user_req, group=group)

            out = {
                "ack": True,
                "msg": "Authentication successful.",
                "data": {
                    "token": token.key
                }
            }
            return HttpResponse(
                json.dumps(out),
                status=200,
                content_type="application/json"
            )
        except Exception as e:
            out = {
                "ack": False,
                "msg": "Authentication failed.",
            }
            return HttpResponse(
                json.dumps(out),
                status=400,
                content_type="application/json"
            )
    else:
        out = {
            "ack": False,
            "msg": "Authentication failed."
        }
        return HttpResponse(
            json.dumps(out),
            status=400,
            content_type="application/json"
        )


class UserProfileLogoutViewSet(APIView):
    def get(self, request):
        logout(request)
        return Response({
                'msg': 'Logged out.'
            }, status=status.HTTP_200_OK
        )
