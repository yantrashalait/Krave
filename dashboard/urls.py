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

    # for restaurant requests
    path('requests/', views.RequestListView.as_view(), name="request-list"),
    path('requests/<int:pk>/', views.RequestDetailView.as_view(), name="request-detail"),
    path('requests/<int:pk>/accept/', views.accept_request, name="accept-request"),
    path('requests/<int:pk>/decline/', views.decline_request, name="decline-request"),

    # for support information
    path('support/list/', views.ListSupportStaff.as_view(), name="support-staffs"),
]
