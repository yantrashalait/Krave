from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'restaurant_request', views.RestaurantRequestViewSet)
router.register(r'user-profile', views.UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('api-auth-token', views.CustomAuthToken.as_view()),
    path('users/add', views.UserCreationViewSet.as_view(), name='add-user'),

    #apis for categories
    path('category/list', views.CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategorySingleViewSet.as_view(), name='category-single'),

    #apis for meals
    path('meal/list', views.MealViewSet.as_view(), name='meal-list'),
    path('meal/<int:pk>', views.MealSingleViewSet.as_view(), name='meal-detail'),

    #apis for restaurant food category
    path('restaurant/<int:rest_id>/food/category', views.RestaurantFoodCategoryViewSet.as_view(), name='rest-food-cat-list'),
    path('restaurant/<int:rest_id>/food/category/<int:category_id>', views.RestaurantFoodCategorySingleViewSet.as_view(), name='rest-food-cat-detail'),

    # #apis for restaurant meals category
    path('restaurant/<int:rest_id>/meal', views.RestaurantMealViewSet.as_view(), name="rest-meal-list"),
    path('restaurant/<int:rest_id>/meal/<int:meal_id>', views.RestaurantMealSingleViewSet.as_view(), name='rest-meal-detail'),

    # #apis for restaurant
    path('restaurant/list', views.RestaurantViewSet.as_view(), name='restaurant-list'),
    path('restaurant/<int:rest_id>', views.RestaurantSingleViewSet.as_view(), name='restaurant-single'),

    #apis for food menus of a restaurant
    path('menu/list/<int:pk>', views.FoodMenuViewSet.as_view(), name='menu-list'),
    path('food/<int:pk>', views.FoodMenuSingleViewSet.as_view(), name='food-single'),
    path('food/search', views.FoodSearch.as_view(), name='food-search'),
]

urlpatterns += router.urls