from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [

    path('restaurant/register', views.restaurant_register, name="restaurant-register"),

    # for user dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # for registration
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    # restaurant views
    path('restaurant-lists', views.RestaurantListView.as_view(), name="restaurant-list"),
    path('restaurant-detail/<slug:rest_name>', views.RestaurantDetail.as_view(), name='restaurant-detail'),
    path('food-detail/', views.get_food_detail, name='get-food-detail'),

    # food listing views
    # search food
    path('food/search/', views.search, name='search'),
    path('food/list/', views.FoodListView.as_view(), name='food-list'),

    # food cart of user
    path('food/cart/', views.FoodCartListView.as_view(), name='food-cart'),
    path('food/cart/<slug:username>', views.FoodCartListView.as_view(), name='food-cart'),
    path('food/cart/delete/<slug:cart_id>', views.FoodCartDeleteView.as_view(), name="cart-delete"),

    #add to order
    path('order/add/', views.add_to_order, name="add-to-order"),
    path('order/place/', views.place_order, name="place-order"),

    path('process-payment/', views.process_payment, name="process-payment"),
    path('charge', views.charge, name="charge"),
]
