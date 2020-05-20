from django.shortcuts import get_object_or_404
from .models import Delivery
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from userrole.models import UserRole
from core.models import Order

User = get_user_model()

@receiver(post_save, sender=Delivery)
def delivery_assigned_notification(sender, instance, created, **kwargs):
    pass


post_save.connect(order_prepared_notification, sender=Order)
post_save.connect(delivery_assigned_notification, sender=Delivery)
