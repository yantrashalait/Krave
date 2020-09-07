from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.db import transaction
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.decorators import api_view

from api.permissions import IsUserOrder
from delivery.models import DeliveryTrack, Delivery
from user.models import UserLocationTrack
from api.serializers.delivery_man import DeliveryManLocationSerializer, DeliveryManOrderSerializer, UserInfoSerializer

User = get_user_model()


class DeliveryManSetLocationViewSet(CreateAPIView):
    serializer_class = DeliveryManLocationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        if 'latitude' not in validated_data or validated_data.get('latitude') == 0:
            return Reponse({
                'status': False,
                'msg': {
                    'latitude': ['Latitude not valid.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        if 'longitude' not in validated_data or validated_data.get('longitude') == 0:
            return Response({
                'status': False,
                'msg': {
                    'longitude': ['Longitude not valid.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(validated_data.get('latitude'), float) and isinstance(validated_data.get('longitude'), float):
            latitude = validated_data.get('latitude', 0.0)
            longitude = validated_data.get('longitude', 0.0)
            location = Point(latitude, longitude)
            tracked_date = datetime.now()
            user_location, created = UserLocationTrack.objects.get_or_create(user=request.user)
            user_location.last_location_point = location
            user_location.longitude = longitude
            user_location.latitude = latitude
            user_location.tracked_date = tracked_date
            user_location.save()
            return Response({
                'status': True,
                'msg': 'Successfully added'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'msg': {
                    'points': ['Latitude and longitude should be of float type.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class DMAssignedOrders(ListAPIView):
    serializer_class = DeliveryManOrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    model = Delivery

    def get_queryset(self, *args, **kwargs):
        return Delivery.objects.filter(delivery_man=self.request.user)

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserDeliveryTrack(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUserOrder]

    def get(self, *args, **kwargs):
        id_string = self.request.GET.get("id_string")
        delivery = get_object_or_404(Delivery, tracking_code=id_string)
        self.check_object_permissions(self.request, delivery)
        last_location = delivery.delivery_man.location
        if last_location:
            longitude = last_location.longitude
            latitude = last_location.latitude
            data = {
                'longitude': longitude,
                'latitude': latitude,
                'status': delivery.status
            }
            return Response({
                'status': True,
                'data': data
            })
        else:
            data = {
                "status": delivery.status
            }
            return Response({
                "status": True,
                'data': data,
            })


class UserInfoVS(RetrieveAPIView):
    serializer_class = UserInfoSerializer
    model = User

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, id=self.kwargs.get('pk'))

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "status": True,
            "data": serializer.data
        })
