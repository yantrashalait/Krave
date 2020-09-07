from rest_framework import serializers

from django.contrib.auth import get_user_model

from delivery.models import Delivery, DeliveryTrack
from user.models import UserLocationTrack
from api.serializers.order import OrderListSerializer

User = get_user_model()


class DeliveryManLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class DeliveryManOrderSerializer(serializers.ModelSerializer):
    order = OrderListSerializer()

    class Meta:
        model = Delivery
        fields = ('order', 'tracking_code', 'status')


class DeliveryLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    

class UserInfoSerializer(serializers.Serializer):
    contact = serializers.SerializerMethodField(read_only=True)
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'contact')

    def get_contact(self, obj):
        return obj.profile.contact