from django.db import models
from django.conf import settings


class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="device", on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=255)
    added_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
