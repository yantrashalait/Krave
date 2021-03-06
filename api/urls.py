from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views
from api.viewsets import user_auth as auth_views
from api.viewsets import food as food_views
from api.viewsets import restaurant as restaurant_views
from api.viewsets import order as order_views
from api.viewsets import delivery_man as delivery_views

router = SimpleRouter()
router.register(r'restaurant_request', views.RestaurantRequestViewSet)


urlpatterns = [
    path('api-auth-token', auth_views.CustomAuthToken.as_view()),
    url(r'^exchange-token/(?P<backend>[^/]+)$', auth_views.exchange_token, name="social-login"),
    path('users/add', auth_views.UserCreationViewSet.as_view(), name='add-user'),
    path('user/profile', auth_views.UserProfileViewSet.as_view(), name="user-profile"),
    path('logout/', auth_views.UserProfileLogoutViewSet.as_view(), name='user-logout'),

    # apis for categories
    path('category/list', food_views.AllCategoryListViewSet.as_view(), name='category-list'),
    path('category/<int:category_id>', food_views.CategoryDetailViewSet.as_view(), name='category-single'),
    path('category/<int:category_id>/foods', food_views.CategoryFoodListViewSet.as_view(), name='category-food-list'),

    # today's deals
    path('today-deals', food_views.TodaysDealViewSet.as_view(), name="today-deals"),

    path('food/list', food_views.FoodListViewSet.as_view(), name='food-search'),

    path('food/<int:food_id>', food_views.FoodDetailViewSet.as_view(), name='food-single'),
    path('food/<int:food_id>/extras', food_views.FoodExtraDetailViewSet.as_view(), name='food-single-extras'),
    path('food/<int:food_id>/style', food_views.FoodStyleDetailViewSet.as_view(), name='food-single-style'),
    path('food/<int:food_id>/get/review', food_views.FoodReviewViewSet.as_view(), name='food-review'),
    path('food/<int:food_id>/get/rating', food_views.FoodRatingViewSet.as_view(), name='food-rating'),
    path('food/<int:food_id>/post/review', food_views.FoodReviewPostViewSet.as_view(), name='food-review-post'),
    path('food/<int:food_id>/post/rating', food_views.FoodRatingPostViewSet.as_view(), name='food-rating-post'),
    path('food/trending', food_views.TrendingFoodListVS.as_view(), name="trending-foods"),

    path('favourites', food_views.UserFavouriteVS.as_view(), name="favourite-list"),
    path('food/<int:food_id>/favourite/add', food_views.add_to_favourite, name="add-to-favourite"),
    path('food/<int:food_id>/favourite/delete', food_views.delete_favourite, name="remove-from-favourite"),

    # apis for restaurant food category
    path('restaurant/<int:rest_id>/food/category', views.RestaurantFoodCategoryViewSet.as_view(), name='rest-food-cat-list'),
    path('restaurant/<int:rest_id>/food/category/<int:category_id>', views.RestaurantFoodCategorySingleViewSet.as_view(), name='rest-food-cat-detail'),

    # apis for restaurant
    path('restaurant/list', restaurant_views.RestaurantListViewSet.as_view(), name='restaurant-list'),
    path('restaurant/popular', restaurant_views.PopularRestaurantListVS.as_view(), name='popular-restaurant'),
    path('restaurant/<int:rest_id>', restaurant_views.RestaurantDetailViewSet.as_view(), name='restaurant-single'),
    path('restaurant/<int:rest_id>/popular-dishes', restaurant_views.RestaurantPopularDishesViewSet.as_view(), name="restaurant-popular-dishes"),
    path('restaurant/<int:rest_id>/food/list', restaurant_views.RestaurantFoodListViewSet.as_view(), name="restaurant-food-list"),
    path('restaurant/<int:restaurant_id>/get/review', restaurant_views.RestaurantReviewViewSet.as_view(), name='restaurant-review'),
    path('restaurant/<int:restaurant_id>/get/rating', restaurant_views.RestaurantRatingViewSet.as_view(), name='restaurant-rating'),
    path('restaurant/<int:restaurant_id>/post/review', restaurant_views.RestaurantReviewPostViewSet.as_view(), name='restaurant-review-post'),
    path('restaurant/<int:restaurant_id>/post/rating', restaurant_views.RestaurantRatingPostViewSet.as_view(), name='restaurant-rating-post'),

    # cart and order
    path('add-to-cart', order_views.AddToCartViewSet.as_view(), name="add-to-cart"),
    path('cart/list', order_views.CartListViewSet.as_view(), name="cart-list"),
    path('cart/edit/<int:cart_id>', order_views.CartEditViewSet.as_view(), name="cart-edit"),
    path('place-order', order_views.OrderPlaceViewSet.as_view(), name="place-order"),
    path('order/list', order_views.OrderListViewSet.as_view(), name="order-list"),
    path('order/<int:pk>/detail', order_views.OrderDetailViewSet.as_view(), name="order-detail"),
    path('order/history', order_views.OrderHistoryViewSet.as_view(), name="order-history"),
    path('order/ongoing/history', order_views.OrderOngoingHistoryViewSet.as_view(), name="order-ongoing-history"),
    path('order/<int:order_id>/status/edit', order_views.EditOrderStatusViewSet.as_view(), name="edit-order-status"),

    # urls for delivery person
    path('set-location', delivery_views.DeliveryManSetLocationViewSet.as_view(), name="set-location"),
    path('assigned-orders', delivery_views.DMAssignedOrders.as_view(), name="dm-assigned-orders"),
    path('delivery/track', delivery_views.UserDeliveryTrack.as_view(), name="delivery-track"),

    path('user/<int:pk>/info', delivery_views.UserInfoVS.as_view(), name="user-info"),
]

urlpatterns += router.urls
