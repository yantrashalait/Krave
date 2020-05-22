from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),

    # for restaurant information
    path('restaurants/', views.RestaurantListView.as_view(), name="restaurant-list"),
    path('restaurant/<int:pk>/detail/', views.RestaurantDetailView.as_view(), name="restaurant-detail"),
    path('restaurant/<int:pk>/earnings/', views.RestaurantPaymentView.as_view(), name="restaurant-payment"),
]
