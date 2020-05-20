from django.db import models
from django.conf import settings
from core.models import FoodMenu, Restaurant, FoodCart
from django.contrib.gis.db.models import PointField
from core.models import Order
from django.contrib.gis.db.models import PointField


DELIVERY_CHOICES = (
    (0, 'Assigned'),
    (1, 'Ongoing'),
    (2, 'Received')
)

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delivery")
    delivery_man = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="delivery", on_delete=models.SET_NULL, null=True)
    tracking_code = models.CharField(max_length=100)
    status = models.IntegerField()


class DeliveryTrack(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name="track")
    last_location_point = PointField(geography=True, srid=4326, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    @property
    def longitude(self):
        if self.last_location_point:
            return self.last_location_point.x

    @property
    def latitude(self):
        if self.last_location_point:
            return self.last_location_point.y
