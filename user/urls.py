from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('profile', views.userprofile, name="profile"),
    path('profile/edit', views.edit_profile, name="edit-profile"),
]