from django.urls import path, include
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('<int:rest_id>/', views.DashboardView.as_view(), name='dashboard'),
    path('<int:rest_id>/detail/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('<int:rest_id>/detail/edit/', views.RestaurantEditDetailView.as_view(), name='restaurant-detail-edit'),

    path('<int:rest_id>/orders', views.OrderView.as_view(), name='order'),
    path('<int:rest_id>/order/<int:order_id>', views.OrderDetailView.as_view(), name="order-detail"),
    path('<int:rest_id>/orders/accepted', views.AcceptedOrderView.as_view(), name="accepted-order"),

    path('<int:rest_id>/menu', views.MenuListView.as_view(), name='menu-list'),
    path('<int:rest_id>/menu/add-food-item/', views.MenuAddView.as_view(), name='menu-add'),
    path('<int:rest_id>/menu/<int:food_id>/edit', views.MenuEditView.as_view(), name="menu-edit"),
    path('<int:rest_id>/menu/<int:food_id>/delete', views.MenuDeleteView.as_view(), name="menu-delete"),

    path('<int:rest_id>/category', views.CategoryListView.as_view(), name="category-list"),
    path('<int:rest_id>/category/add', views.CategoryCreateView.as_view(), name="category-add"),
    path('<int:rest_id>/category/<int:category_id>/edit', views.CategoryEditView.as_view(), name="category-edit"),
    path('<int:rest_id>/category/<int:category_id>/delete', views.CategoryDeleteView.as_view(), name="category-delete"),

    # password change
    path('password/change', views.change_password, name='change-password'),

    path('order/accept/<int:order_id>', views.accept_order, name="accept-order"),
    path('order/decline/<int:order_id>', views.decline_order, name="decline-order"),
    path('order/ready/<int:order_id>', views.ready_order, name="ready-order"),

    path('order/add/', views.manual_order, name="manual-order"),
    path('cart/', views.FoodCartListView.as_view(), name="food-cart"),
    path('cart/delete/<int:pk>/', views.FoodCartDeleteView.as_view(), name="cart-delete"),

    path('add-order/', views.add_to_order, name='add-to-order'),

    # restaurant earnings
    path('earnings/', views.PaymentListView.as_view(), name="earnings"),
    path('earnings/search/', views.PaymentListSearchView.as_view(), name="earnings-search"),

    path('chef-special/list/', views.list_chef_special, name="chef-special"),
    path('chef-special/<int:pk>/delete/', views.delete_chef_special, name="chef-special-delete"),
    path('chef-special/add/', views.add_chef_special, name="chef-special-add"),

]
