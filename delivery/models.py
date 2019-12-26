from django.db import models
from django.conf import settings
from core.models import FoodMenu, Restaurant, FoodCart
from django.contrib.gis.db.models import PointField
from core.models import Order

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

