from rest_framework import serializers
from core.models import Category, RestaurantCuisine, FoodMenu, FoodExtra, FoodStyle


# BASE_URL = "http://localhost:8000/api/v1"
BASE_URL = "https://krave.yantrashala.com/api/v1"

MEDIA_URL = "https://krave.yantrashala.com"


class CategoryListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('name', 'image', 'detail_url', 'id')

    def get_detail_url(self, obj):
        return BASE_URL + "/category/" + str(obj.id)

    def get_image(self, obj):
        if obj.image:
            return MEDIA_URL + obj.image.url
        else:
            return ""


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
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'food', 'image')

    def get_image(self, obj):
        if obj.image:
            return MEDIA_URL + obj.image.url
        else:
            return ""


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
