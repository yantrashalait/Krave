from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [

    # for restaurant requests
    path('requests/', views.RequestList.as_view(), name='request-list'),
    path('request-detail/<int:pk>', views.RequestDetail.as_view(), name='request-detail'),
    path('requests/accept/<int:pk>', views.acceptRequest, name='accept-request'),
    path('request/reject/<int:pk>', views.rejectRequest, name='reject-request'),

    # for user dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),

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

]