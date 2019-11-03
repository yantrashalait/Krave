from django.db import models
from django.contrib.gis.db.models import PointField
from datetime import datetime


"""
    Restaurant model stores the details about restaurant profile that is visible to the public.
"""
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    contact = models.CharField(max_length=20)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    delivery_upto = models.TextField(help_text="Where do you deliver?")

    @property
    def longitude(self):
        if self.location:
            return self.location.x
    
    @property
    def latitude(self):
        if self.location:
            return self.location.y        

    def __str__(self):
        return self.name


"""
    Food categories are the types of food(e.g. Indian, Chinese, Nepali, etc.)
"""
class FoodCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


"""
    It stores the detail about the food served by a specific restaurant.
"""
class FoodMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu")
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="food")
    name = models.CharField(max_length=255)
    recipe = models.TextField(null=True)
    old_price = models.FloatField()
    new_price = models.FloatField()
    # The preparation time of each food may vary according to the restaurant.
    preparation_time = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class RestaurantRequest(models.Model):
    name = models.CharField(max_length=255)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    name_of_owner = models.CharField(max_length=255)
    email_of_owner = models.EmailField()
    contact = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=255, help_text='registration number of restaurant')
    message = models.TextField(help_text="Explain in short why do you want to be registered here?")
    requested_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    @property
    def longitude(self):
        if self.location:
            return self.location.x
    
    @property
    def latitude(self):
        if self.location:
            return self.location.y

    def __str__(self):
        return self.name




