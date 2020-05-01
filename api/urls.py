from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views
from api.viewsets import user_auth as auth_views
from api.viewsets import food as food_views
from api.viewsets import restaurant as restaurant_views

router = SimpleRouter()
router.register(r'restaurant_request', views.RestaurantRequestViewSet)


urlpatterns = [
    path('api-auth-token', auth_views.CustomAuthToken.as_view()),
    path('users/add', auth_views.UserCreationViewSet.as_view(), name='add-user'),
    path('user/profile', auth_views.UserProfileViewSet.as_view(), name="user-profile"),

    #apis for categories
    path('category/list', food_views.AllCategoryListViewSet.as_view(), name='category-list'),
    path('category/<int:category_id>', food_views.CategoryDetailViewSet.as_view(), name='category-single'),

    path('food/list', food_views.FoodListViewSet.as_view(), name='food-search'),

    path('food/<int:food_id>', food_views.FoodDetailViewSet.as_view(), name='food-single'),

    #apis for restaurant food category
    path('restaurant/<int:rest_id>/food/category', views.RestaurantFoodCategoryViewSet.as_view(), name='rest-food-cat-list'),
    path('restaurant/<int:rest_id>/food/category/<int:category_id>', views.RestaurantFoodCategorySingleViewSet.as_view(), name='rest-food-cat-detail'),

    # #apis for restaurant
    path('restaurant/list', restaurant_views.RestaurantListViewSet.as_view(), name='restaurant-list'),
    path('restaurant/<int:rest_id>', restaurant_views.RestaurantDetailViewSet.as_view(), name='restaurant-single'),

    # apis for restaurant food
    path('restaurant/<int:rest_id>/food/list', views.RestaurantFoodListViewSet.as_view(), name="restaurant-food-list"),
    

    #apis for food cart
    path('cart/<int:user_id>', views.UserCartViewSet.as_view(), name='add-to-cart'),
    path('cart/<int:user_id>/<int:cart_id>', views.UserCartSingleViewSet.as_view(), name='user-cart-single'),

]

urlpatterns += router.urls
