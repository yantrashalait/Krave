from django.urls import path, include
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('<int:rest_id>/', views.DashboardView.as_view(), name='dashboard'),
    path('<int:rest_id>/detail/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),

    path('<int:rest_id>/orders', views.OrderView.as_view(), name='order'),
    path('<int:rest_id>/order/<int:order_id>', views.OrderDetailView.as_view(), name="order-detail"),
    path('<int:rest_id>/orders/accepted', views.AcceptedOrderView.as_view(), name="accepted-order"),

    path('<int:rest_id>/menu', views.MenuListView.as_view(), name='menu-list'),
    path('<int:rest_id>/menu/<int:food_id>/edit', views.MenuEditView.as_view(), name="menu-edit"),
    path('<int:rest_id>/menu/<int:food_id>/delete', views.MenuDeleteView.as_view(), name="menu-delete"),

    # password change
    path('password/change', views.change_password, name='change-password'),

    path('order/accept/<int:order_id>', views.accept_order, name="accept-order"),
    path('order/ready/<int:order_id>', views.ready_order, name="ready-order"),


]
