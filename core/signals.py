from django.shortcuts import get_object_or_404
from .models import Order, Notification, Restaurant
from django.dispatch import receiver
from django.db.models.signals import post_save , m2m_changed
from django.contrib.auth import get_user_model
from userrole.models import UserRole

User = get_user_model()


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    try:
        if instance._runsignal:
            user = instance.user
            noti = Notification(content_object=user, order=instance, title="Order Placed")
            for item in instance.cart.all():
                restaurant = item.restaurant

            userrole = UserRole.objects.filter(restaurant=restaurant)
            destination = userrole[0].user
            description = "User " + user.username + " placed an order."
            noti.destination = destination
            noti.description = description
            noti.save()
    except:
        pass


@receiver(post_save, sender=Order)
def order_approved_notification(sender, instance, created, **kwargs):
    try:
        if instance._approved:
            user = instance.user
            for item in instance.cart.all():
                restaurant = item.restaurant
            userrole = UserRole.objects.get(restaurant=restaurant)
            source_user = userrole.user
            noti = Notification(content_object=source_user, order=instance, title="Order Approved")
            destination = user
            description = "Your order '" + instance.id_string +"' has been accepted."
            noti.description = description
            noti.destination = destination
            noti.save()
    except:
        pass


@receiver(post_save, sender=Order)
def order_prepared_notification(sender, instance, created, **kwargs):
    try:
        if instance._prepared:
            pass
    except:
        pass


post_save.connect(order_created_notification, sender=Order)
post_save.connect(order_approved_notification, sender=Order)
