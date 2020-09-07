from rest_framework import serializers
from core.models import Restaurant, RestaurantCuisine, RestaurantFoodCategory, RestaurantImage, Order, FoodCart, FoodExtra
from django.db.models import Q
from api.serializers.food import FoodDetailSerializer, FoodExtraSerializer, FoodStyleSerializer

# BASE_URL = "http://localhost:8000/api/v1"
BASE_URL = "http://krave.yantrashala.com/api/v1"


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
    user = serializers.ReadOnlyField(source="user.id")
    added_on = serializers.ReadOnlyField()
    checked_out = serializers.ReadOnlyField()
    total_price = serializers.SerializerMethodField(read_only=True)
    restaurant = serializers.ReadOnlyField(source="restaurant.id")

    class Meta:
        model = FoodCart
        exclude = ("modified_on", "session_key")
        extra_kwargs = {'number_of_food': {'required': True}, 'style': {'required': True}, 'extras': {'required': False}}

    def get_total_price(self, obj):
        return obj.get_total

    def validate_number_of_food(self, value):
        if not isinstance(value, int) or value < 1:
            raise serializers.ValidationError("Please insert a valid quantity")
        return value

    def validate_restaurant(self, value):
        try:
            restaurant = Restaurant.objects.get(id=value)
            if FoodCart.objects.filter(~Q(restaurant=restaurant), checked_out=False).exists():
                raise serializers.ValidationError("You have already ordered food from another restaurant. To place order from another restaurant, you need to checkout the first order.")
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError("This restaurant does not exist.")


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("note", "address_line1", "address_line2", "city", "state", "zip_code", "payment")


class OrderListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'id_string', 'total_price', 'note', 'user_id')

    def get_user(self, obj):
        return obj.foods.last().user.id


class OrderDetailSerializer(serializers.ModelSerializer):
    foods = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'foods', 'status', 'id_string', 'total_price', 'note',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code'
            )

    def get_foods(self, obj):
        foods = []
        for item in obj.cart.all():
            food = {}
            food['food_name'] = item.food.name
            food['price'] = item.food.new_price
            food['image_url'] = item.food.image.url
            food['number'] = item.number_of_food
            if item.style:
                food['style'] = item.style.name_of_style
            if item.extras:
                food['extras'] = [extra.name_of_extra for extra in item.extras.all()]
            foods.append(food)
        return foods
