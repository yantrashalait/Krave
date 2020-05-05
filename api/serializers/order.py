from rest_framework import serializers
from core.models import Restaurant, RestaurantCuisine, RestaurantFoodCategory, RestaurantImage, Order, FoodCart, FoodExtra
from django.db.models import Q
from api.serializers.food import FoodDetailSerializer, FoodExtraSerializer, FoodStyleSerializer


class CartListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    added_on = serializers.ReadOnlyField()
    checked_out = serializers.ReadOnlyField()
    total_price = serializers.SerializerMethodField(read_only=True)
    restaurant = serializers.ReadOnlyField(source="restaurant.id")
    food = FoodDetailSerializer()
    style = FoodStyleSerializer()
    extras = FoodExtraSerializer(many=True)

    class Meta:
        model = FoodCart
        exclude = ("modified_on", "session_key")
        extra_kwargs = {'number_of_food': {'required': True}, 'style': {'required': True}, 'extras': {'required': False}}
    
    def get_total_price(self, obj):
        return obj.get_total


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCart
        exclude = ("modified_on", "session_key", "food", "restaurant", "added_on", "checked_out", "style", "extras")
        extra_kwargs = {"number_of_food": {"required": True}}
    
    def validate_number_of_food(self, value):
        if not isinstance(value, int) or value < 1:
            raise serializers.ValidationError("Please insert a valid quantity")
        return value


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    total_price = serializers.ReadOnlyField()
    id_string = serializers.ReadOnlyField()
    delivery_person = serializers.ReadOnlyField(source="user.id")
    paid = serializers.ReadOnlyField()
    cart = CartListSerializer(many=True)
    payment_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ("cart", "last_modified", "created_at", "added_date", "delivery_person", "paid")

