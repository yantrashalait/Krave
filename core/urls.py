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
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),

    #restaurant views
    path('restaurant-detail/', views.RestaurantDetail.as_view(), name='restaurant-detail'),
]