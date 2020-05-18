from rest_framework import serializers

from django.contrib.auth import get_user_model

from delivery.models import Delivery, DeliveryTrack
from user.models import UserLocationTrack

User = get_user_model()


class DeliveryManLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
