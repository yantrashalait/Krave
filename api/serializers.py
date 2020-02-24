from rest_framework import serializers
from core.models import Restaurant, RestaurantRequest, FoodMenu, RestaurantFoodCategory, \
    FoodCart, RestaurantCuisine, RestaurantImage, FoodStyle, FoodExtra, Cuisine
from user.models import User, UserProfile
from django.conf import settings
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError


base_url = 'http://localhost:8000/api/v1/'
# base_url = 'https://www.krave.yantrashala.com/api/v1/'



class FoodMenuSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True, max_length=500)
    image = serializers.ImageField(required=True)
    preparation_time = serializers.CharField(required=True, max_length=50)
    detail_url = serializers.SerializerMethodField()
    restaurant = serializers.ReadOnlyField(source='restaurant.name')
    category = serializers.ReadOnlyField(source='category.category')

    class Meta:
        model = FoodMenu
        fields = ('id', 'name', 'restaurant', 'restaurant_id', 'category_id', 'category', 'description', 'image',
        'ingredients', 'old_price', 'new_price', 'preparation_time', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + 'food/' + str(obj.id)


class CategorySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    restaurant = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'restaurant_id', 'restaurant', 'category', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + 'category/' + str(obj.id)


class CategorySingleSerializer(serializers.ModelSerializer):
    food = FoodMenuSerializer(many=True, read_only=True)
    restaurant = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = RestaurantFoodCategory
        fields = ('restaurant', 'restaurant_id', 'category', 'food')


class FoodExtraSerializer(serializers.ModelSerializer):
    food = serializers.ReadOnlyField(source="food.name")

    class Meta:
        model = FoodExtra
        fields = ('id', 'name_of_extra', 'cost', 'food_id', 'food')


class FoodStyleSerializer(serializers.ModelSerializer):
    food = serializers.ReadOnlyField(source="food.name")

    class Meta:
        model = FoodStyle
        fields = ('id', 'name_of_style', 'cost', 'food_id', 'food')


class FoodMenuDetailSerializer(serializers.ModelSerializer):
    styles = FoodStyleSerializer(many=True)
    extras = FoodExtraSerializer(many=True)
    restaurant = serializers.ReadOnlyField(source="restaurant.name")
    category = serializers.ReadOnlyField(source="category.category")

    class Meta:
        model = FoodMenu
        fields = ('id', 'name', 'restaurant', 'restaurant_id', 'category_id', 'category', 'description', 'image',
        'ingredients', 'old_price', 'new_price', 'preparation_time', 'styles', 'extras')


class RestaurantFoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'category', 'restaurant')


class RestaurantDetailFoodCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    create_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    foods = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'category', 'create_url', 'detail_url', 'foods')

    def get_create_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/food/category/'

    def get_detail_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/food/category/' + str(obj.category.id) + '/'

    def get_foods(self, obj):
        foods = FoodMenu.objects.filter(restaurant=obj.restaurant, category_id=obj.category.id)
        return FoodMenuSerializer(foods, many=True).data


class RestaurantListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'opening_time', 'closing_time', 'delivery_upto',
        'location_point', 'street', 'town', 'state', 'zip_code', 'logo', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + 'restaurant/' + str(obj.id)


class RestaurantDetailSerializer(serializers.ModelSerializer):
    cuisines = serializers.SerializerMethodField()
    food_category = RestaurantFoodCategorySerializer(many=True, read_only=True)
    menu = FoodMenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'opening_time', 'closing_time', 'delivery_upto',
        'location_point', 'street', 'town', 'state', 'zip_code', 'logo', 'owner',
        'delivery_charge', 'registration_number', 'email', 'delivery_time', 'cuisines',
        'food_category', 'menu')

    def get_cuisines(self, obj):
        rest_cuisine = RestaurantCuisine.objects.get(restaurant=obj)
        return rest_cuisine.cuisine.all().values('name')


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ('image')


class RestaurantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRequest
        exclude = ('accepted',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=500, required=True)
    username = serializers.CharField(max_length=500, required=True)
    password = serializers.CharField(min_length=8)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        return user

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("User with this username already exists.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return email

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_user(self, object):
        return object.user.username


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCart
        fields = '__all__'
