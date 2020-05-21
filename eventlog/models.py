from django.db import models
from django.db.models import Q
from jsonfield import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from core.models import Restaurant, Order

class EventLog(models.Model):
    ACTION_TYPES = (
        (1, 'Order Placed'),
        (2, 'Order Approved'),
        (3, 'Order Cancelled'),
        (4, 'Order Prepared'),
        (5, 'Order Picked Up'),
        (6, 'Order Delivered'),
        (7, 'Delivery Assigned'),
        (8, 'Delivery Rejected'),
    )

    type = models.IntegerField(default=0, choices=ACTION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="log", null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="log", null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="log", null=True, on_delete=models.CASCADE)
    extra_json = JSONField(blank=True, null=True, default=None)
    receipent = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="receipent_log", null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    event_name = models.CharField(max_length=255, blank=True)
