from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('requests/', views.RequestList.as_view(), name='request-list'),
    path('request-detail/<int:pk>', views.RequestDetail.as_view(), name='request-detail'),
    path('requests/accept/<int:pk>', views.acceptRequest, name='accept-request'),
    path('request/reject/<int:pk>', views.rejectRequest, name='reject-request'),
]