from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'restaurant', views.RestaurantViewSet, basename='restaurant')
router.register(r'restaurant_request', views.RestaurantRequestViewSet)
router.register(r'user-profile', views.UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('api-auth-token/', views.CustomAuthToken.as_view()),
    path('users/add/', views.UserCreationViewSet.as_view(), name='add-user'),
    path('category/list/', views.CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategorySingleViewSet.as_view(), name='category-single'),
    path('menu/list/<int:pk>/', views.FoodMenuViewSet.as_view(), name='menu-list'),
    path('food/<int:pk>/', views.FoodMenuSingleViewSet.as_view(), name='food-single'),
    path('food/search/', views.FoodSearch.as_view(), name='food-search'),
]

urlpatterns += router.urls