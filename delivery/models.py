from django.db import models
from django.conf import settings
from core.models import FoodMenu, Restaurant
from django.contrib.gis.db.models import PointField


ORDER_STATUS = (
    (0, 'Active'),
    (1, 'Deleted'),
    (2, 'Ready'),
    (3, 'Delivered')
)

class Order(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.SET_NULL, null=True, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    location = PointField(geography=True, srid=4326)
    order_number = models.CharField(max_length=255)
    status = models.IntegerField(choices=ORDER_STATUS)

    def __str__(self):
        return self.food.name + ' ' + self.ordered_by.username


DELIVERY_CHOICES = (
    (0, 'Assigned'),
    (1, 'Ongoing'),
    (2, 'Received')
)

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delivery")
    delivery_time = models.TimeField()
    delivery_man = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="delivery", on_delete=models.SET_NULL, null=True)
    tracking_code = models.CharField(max_length=100)
    status = models.IntegerField()

