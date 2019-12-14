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
    # path('category/list', views.CategoryViewSet.as_view(), name='category-list'),
    # path('category/<int:pk>', views.CategorySingleViewSet.as_view(), name='category-single'),

    #apis for restaurant food category
    path('restaurant/<int:rest_id>/food/category', views.RestaurantFoodCategoryViewSet.as_view(), name='rest-food-cat-list'),
    path('restaurant/<int:rest_id>/food/category/<int:category_id>', views.RestaurantFoodCategorySingleViewSet.as_view(), name='rest-food-cat-detail'),

    # #apis for restaurant
    path('restaurant/list', views.RestaurantViewSet.as_view(), name='restaurant-list'),
    path('restaurant/<int:rest_id>', views.RestaurantSingleViewSet.as_view(), name='restaurant-single'),

    #apis for food menus of a restaurant
    path('menu/list/<int:rest_id>', views.FoodMenuViewSet.as_view(), name='menu-list'),
    path('food/<int:food_id>', views.FoodMenuSingleViewSet.as_view(), name='food-single'),
    path('food/search', views.FoodSearch.as_view(), name='food-search'),

    #apis for food cart
    path('cart/<int:user_id>', views.UserCartViewSet.as_view(), name='add-to-cart'),
    path('cart/<int:user_id>/<int:cart_id>', views.UserCartSingleViewSet.as_view(), name='user-cart-single'),

]

urlpatterns += router.urls