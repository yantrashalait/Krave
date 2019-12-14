from rest_framework import serializers
from core.models import Restaurant, RestaurantRequest, FoodMenu, RestaurantFoodCategory, \
    FoodCart, RestaurantCuisine, RestaurantImage
from user.models import User, UserProfile
from django.conf import settings
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError


# base_url = 'http://localhost:8000/api/v1/'
base_url = 'http://157.245.213.171:8000/api/v1/'


class RestaurantFoodCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'category', 'restaurant')
    
    def validate(self, data):
        if RestaurantFoodCategory.objects.filter(category=data['category'], restaurant=data['restaurant']).exists():
            raise ValidationError("Category already assigned to the restaurant.")
        return data


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


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'contact', 'opening_time', 'closing_time', 'delivery_upto', 'location')


class RestaurantCuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCuisine
        fields = ('name')


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ('image')


class RestaurantSingleSerializer(serializers.ModelSerializer):
    food_category = serializers.SerializerMethodField()
    cuisine = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('name', 'contact', 'logo', 'opening_time', 'closing_time', 'delivery_upto', 
        'location', 'food_category', 'cuisine', 'delivery_charge', 'images')

    def get_food_category(self, obj):
        categories = RestaurantFoodCategory.objects.filter(restaurant=obj)
        return RestaurantDetailFoodCategorySerializer(categories, many=True).data
    
    def get_cuisine(self, obj):
        cuisines = RestaurantCuisine.objects.filter(restaurant=obj)
        return RestaurantCuisineSerializer(cuisines, many=True).data

    def get_images(self, obj):
        images = RestaurantImage.objects.filter(restaurant=obj)
        return  RestaurantImageSerializer(images, many=True).data


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


class FoodMenuSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    description = serializers.CharField(required=True, max_length=500)
    image = serializers.ImageField(required=True)
    preparation_time = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = FoodMenu
        fields = ('id', 'name', 'restaurant', 'category', 'description', 
        'image_url', 'image', 'ingredients', 'old_price', 'new_price', 'preparation_time')
    
    def get_image_url(self, obj):
        return base_url + str(obj.image)


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCart
        fields = '__all__'