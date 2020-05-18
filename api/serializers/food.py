from rest_framework import serializers
from core.models import RestaurantFoodCategory, RestaurantCuisine, FoodMenu, FoodExtra, FoodStyle


# BASE_URL = "http://localhost:8000/api/v1"
BASE_URL = "http://krave.yantrashala.com/api/v1"

class CategoryListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = RestaurantFoodCategory
        fields = "__all__"

    def get_detail_url(self, obj):
        return basBASE_URLe_url + "/category/" + str(obj.id)


class FoodFilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(deleted=False)
        return super(FoodFilteredListSerializer, self).to_representation(data)


class FoodMenuListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    restaurant_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        list_serializer_class = FoodFilteredListSerializer
        model = FoodMenu
        exclude = ("created_date", "modified_date", "deleted", "category")

    def get_detail_url(self, obj):
        return BASE_URL + "/food/" + str(obj.id)

    def get_restaurant_name(self, obj):
        return obj.restaurant.name


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    food = FoodMenuListSerializer(many=True)

    class Meta:
        model = RestaurantFoodCategory
        fields = "__all__"


class FoodExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExtra
        exclude = ("food", )


class FoodStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodStyle
        exclude = ('food', )


class FoodDetailSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    styles = FoodStyleSerializer(many=True)
    extras = FoodExtraSerializer(many=True)

    class Meta:
        model = FoodMenu
        exclude = ("created_date", "modified_date", "deleted")

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

    def get_category_name(self, obj):
        return obj.category.category
