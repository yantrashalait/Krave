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

    path('change-password/', views.change_password, name="change-password"),

    # for support information
    path('support/list/', views.SupportStaffListView.as_view(), name="support-staffs"),
    path('support/create/', views.staff_create, name="staff-create"),
    path('support/<int:pk>/detail/', views.SupportStaffDetailView.as_view(), name="support-detail"),

    # for delivery person information
    path('delivery-person/list/', views.DeliveryPersonListView.as_view(), name="delivery-person-list"),
    path('delivery-person/create/', views.delivery_person_create, name="delivery-person-create"),
    path('delivery-person/<int:pk>/detail/', views.DeliveryPersonDetailView.as_view(), name="delivery-person-detail"),
]
