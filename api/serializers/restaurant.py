from rest_framework import serializers
from core.models import Restaurant, RestaurantCuisine, RestaurantFoodCategory, RestaurantImage


# BASE_URL = "http://localhost:8000/api/v1"
BASE_URL = "https://krave.yantrashala.com/api/v1"


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        exclude = ("restaurant", "image")


class RestaurantListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    images = RestaurantImageSerializer(many=True)

    class Meta:
        model = Restaurant
        exclude = ("location_point", "joined_date")
    
    def get_detail_url(self, obj):
        return BASE_URL + "/restaurant/" + str(obj.pk)
    
    def get_rating(self, obj):
        # static for now
        return 4.0
    
    def get_review_count(self, obj):
        return obj.restaurant_review.count()


class RestaurantDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    images = RestaurantImageSerializer(many=True)
    cuisines = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        exclude = ("joined_date", )
    
    def get_rating(self, obj):
        # static for now
        return 4.0
    
    def get_review_count(self, obj):
        return obj.restaurant_review.count()
    
    def get_cuisines(self, obj):
        cuisine_list = []
        try:
            rest_cuisine = RestaurantCuisine.objects.get(restaurant=obj)
            for item in rest_cuisine.cuisine.all():
                cuisine_list.append(item.name)
        except RestaurantCuisine.DoesNotExist:
            pass
        return cuisine_list
