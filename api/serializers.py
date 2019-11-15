from rest_framework import serializers
from core.models import Restaurant, RestaurantRequest, FoodCategory, FoodMenu, MealType, \
    RestaurantMealType, RestaurantFoodCategory
from user.models import User, UserProfile
from django.conf import settings
from rest_framework.validators import UniqueValidator

# base_url = 'http://localhost:8000/api/v1/'
base_url = 'http://157.245.213.171:8000/api/v1/'

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'


class RestaurantFoodCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'category', 'category_name')
    
    def get_category_name(self, obj):
        return obj.category.name


class RestaurantDetailFoodCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    create_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    foods = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodCategory
        fields = ('id', 'category', 'category_name', 'create_url', 'detail_url', 'foods')
    
    def get_category_name(self, obj):
        return obj.category.name

    def get_create_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/food/category/'
    
    def get_detail_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/food/category/' + str(obj.category.id) + '/'

    def get_foods(self, obj):
        foods = FoodMenu.objects.filter(restaurant=obj.restaurant, category_id=obj.category.id)
        return FoodMenuSerializer(foods, many=True).data


class RestaurantMealSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantMealType
        fields = ('id', 'meal_type', 'restaurant', 'meal_name')

    def get_meal_name(self, obj):
        return obj.meal_type.name


class RestaurantDetailMealSerializer(serializers.ModelSerializer):
    meal_name = serializers.SerializerMethodField()
    create_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    foods = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantMealType
        fields = ('id', 'meal_type', 'meal_name', 'restaurant', 'create_url', 'detail_url', 'foods')

    def get_meal_name(self, obj):
        return obj.meal_type.name

    def get_create_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/meal/'
    
    def get_detail_url(self, obj):
        return base_url + 'restaurant/' + str(obj.restaurant.id) + '/meal/' + str(obj.meal_type.id) + '/'

    def get_foods(self, obj):
        foods = FoodMenu.objects.filter(restaurant=obj.restaurant, meal_type=obj.meal_type)
        return FoodMenuSerializer(foods, many=True).data


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'contact', 'opening_time', 'closing_time', 'delivery_upto', 'location')


class RestaurantSingleSerializer(serializers.ModelSerializer):
    food_category = serializers.SerializerMethodField()
    meal_type = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('name', 'contact', 'opening_time', 'closing_time', 'delivery_upto', 'location', 'food_category', 'meal_type')

    def get_food_category(self, obj):
        categories = RestaurantFoodCategory.objects.filter(restaurant=obj)
        return RestaurantDetailFoodCategorySerializer(categories, many=True).data

    def get_meal_type(self, obj):
        meals = RestaurantMealType.objects.filter(restaurant=obj)
        return RestaurantDetailMealSerializer(meals, many=True).data


class RestaurantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRequest
        exclude = ('accepted',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
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

    class Meta:
        model = FoodMenu
        fields = ('id', 'name', 'restaurant', 'meal_type', 'category', 'description', 
        'image_url', 'image', 'recipe', 'old_price', 'new_price', 'preparation_time')
    
    def get_image_url(self, obj):
        return base_url + str(obj.image)