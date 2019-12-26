from django.urls import path, include
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('detail/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('edit', views.RestaurantEditView.as_view(), name='restaurant-edit'),
    path('orders', views.OrderView.as_view(), name='order'),
    path('menu', views.MenuListView.as_view(), name='menu-list'),
    path('orders/accepted', views.AcceptedOrderView.as_view(), name="accepted-order"),

]