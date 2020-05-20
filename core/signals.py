from django.shortcuts import get_object_or_404
from .models import Order, Notification, Restaurant
from django.dispatch import receiver
from django.db.models.signals import post_save , m2m_changed
from django.contrib.auth import get_user_model
from userrole.models import UserRole

User = get_user_model()


@receiver(post_save, sender=Order)
def order_event_notification(sender, instance, created, **kwargs):
    try:
        if instance._runsignal:
            user = instance.user
            noti = Notification(content_object=user, order=instance, title="Order Placed")
            restaurant = instance.cart.first().restaurant

            userrole = UserRole.objects.filter(restaurant=restaurant)
            destination = userrole[0].user
            description = "User " + user.username + " placed an order."
            noti.destination = destination
            noti.description = description
            noti.save()
    except Exception as e:
        print(e)

    try:
        if instance._approved:
            restaurant = instance.cart.first().restaurant
            userrole = UserRole.objects.get(restaurant=restaurant)
            source_user = userrole.user
            description = "Your order '" + instance.id_string +"' has been accepted."
            noti = Notification.objects.create(
                content_object=source_user,
                order=instance,
                title="Order Approved",
                destination=instance.user,
                description=description
                )
    except Exception as e:
        print(e)

    try:
        if instance._prepared:
            restaurant = instance.cart.first().restaurant
            userrole = UserRole.objects.get(restaurant=restaurant)
            source_user = userrole.user
            description = "Your order '" + instance.id_string + "' has been prepared.'"
            noti = Notification.objects.create(
                content_object=source_user,
                order=instance,
                title="Order Prepared",
                destination_id=instance.user.pk,
                description=description
                )

    except Exception as e:
        print(e)


post_save.connect(order_event_notification, sender=Order)
