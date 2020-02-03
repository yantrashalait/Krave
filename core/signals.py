from django.shortcuts import get_object_or_404
from .models import Order, Notification, Restaurant
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.db.models.signals import post_save 


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        order = get_object_or_404(Order, id=ipn.invoice)
 
        if order.total_cost() == ipn.mc_gross:
            # mark the order as paid
            order.paid = True
            order.save()


@receiver(post_save, sender=Order)
def order_created_notification(sender, **kwargs):
    print(**kwargs)


