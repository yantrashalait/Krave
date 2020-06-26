from rest_framework import serializers
from core.models import Restaurant, RestaurantCuisine, RestaurantFoodCategory, RestaurantImage


# BASE_URL = "http://localhost:8000/api/v1"
BASE_URL = "https://krave.yantrashala.com/api/v1"
MEDIA_URL = "https://krave.yantrashala.com"


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        exclude = ("restaurant", "image")


class RestaurantListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

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

    def get_image(self, obj):
        if obj.images.last():
            if obj.images.last().image:
                return MEDIA_URL + obj.images.last().image.url
            else:
                return ""
        else:
            return ""


class RestaurantDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    cuisines = serializers.SerializerMethodField(read_only=True)
    popular_dishes_url = serializers.SerializerMethodField(read_only=True)
    menu_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

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

    def get_popular_dishes_url(self, obj):
        return BASE_URL + '/restaurant/' + str(obj.pk) + '/popular-dishes'

    def get_menu_url(self, obj):
        return BASE_URL + '/restaurant/' + str(obj.pk) + '/food/list'

    def get_image(self, obj):
        if obj.images.last():
            if obj.images.last().image:
                return MEDIA_URL + obj.images.last().image.url
            else:
                return ""
        else:
            return ""