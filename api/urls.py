from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'restaurant', views.RestaurantViewSet)
router.register(r'restaurant_request', views.RestaurantRequestViewSet)
router.register(r'user-profile', views.UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('api-auth-token/', views.CustomAuthToken.as_view()),
    path('users/add/', views.UserCreationViewSet.as_view(), name='add-user'),
]

urlpatterns += router.urls