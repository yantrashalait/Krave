from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from django.db import transaction
from django.db.models import Q
from rest_framework.decorators import api_view
from django.contrib.gis.geos import Point
from datetime import datetime

from delivery.models import DeliveryTrack, Delivery
from user.models import UserLocationTrack
from api.serializers.delivery_man import DeliveryManLocationSerializer


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
            })

        if 'longitude' not in validated_data or validated_data.get('longitude') == 0:
            return Response({
                'status': False,
                'msg': {
                    'longitude': ['Longitude not valid.']
                }
            })

        if isinstance(validated_data.get('latitude'), float) and isinstance(validated_data.get('longitude'), float):
            latitude = validated_data.get('latitude', 0.0)
            longitude = validated_data.get('longitude', 0.0)
            location = Point(latitude, longitude)
            tracked_date = datetime.now()
            user_location, created = UserLocationTrack.objects.get_or_create(user=request.user)
            user_location.last_location_point = location
            user_location.tracked_date = tracked_date
            return Response({
                'status': True,
                'msg': 'Successfully added'
            })
        else:
            return Response({
                'status': False,
                'msg': {
                    'points': ['Latitude and longitude should be of float type.']
                }
            })
