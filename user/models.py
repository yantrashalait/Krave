from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.db.models import Manager as GeoManager


class User(AbstractUser):
    is_restaurant = models.BooleanField(default=False)
    is_deliveryman = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True, null=True, blank=True) # for delivery man


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/')
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    def __str__(self):
        return self.user.username + ' - ' + 'Profile'


class UserLocationTrack(models.Model):
    geo_objects = GeoManager()

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    last_location_point = PointField(geography=True, srid=4326, blank=True, null=True)
    tracked_date = models.DateTimeField(auto_now_add=True)

    @property
    def longitude(self):
        if self.last_location_point:
            return self.last_location_point.x

    @property
    def latitude(self):
        if self.last_location_point:
            return self.last_location_point.y

    def __str__(self):
        return "Last location of " + self.user.username
