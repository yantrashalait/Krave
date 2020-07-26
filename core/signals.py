from django.shortcuts import get_object_or_404
from .models import Order, Notification, Restaurant, RestaurantPayment
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

            if instance.payment == 2 and instance.paid == True:
                RestaurantPayment.objects.create(restaurant=restaurant, order=instance, payment_amount=instance.total_price)

    except Exception as e:
        print(e)

    try:
        if instance._approved:
            restaurant = instance.cart.first().restaurant
            userrole = UserRole.objects.get(restaurant=restaurant)
            source_user = userrole.user
            description = "Your order '" + instance.id_string + "' has been accepted."
            noti = Notification.objects.create(
                content_object=source_user,
                order=instance,
                title="Order Approved",
                destination=instance.user,
                description=description
                )
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Order Placed"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = instance.user.email
            to_email = instance.user.email

            html = """
                    <html>
                        <head></head>
                        <body>
                            Greetings """ + instance.user.username + """,
                            <br>
                            Your order has been accepted by """ + restaurant.name + """.
                            <p><b>Order Details</b></p>
                            <p>
                                <ul>
                                    <li><b>Order ID</b>: """ + order.id_string + """"</li>
                                    <li><b>Order placed on</b>: """ + order.created_at.strftime("%m/%d/%Y, %H:%M:%S") + """</li>
                                </ul>
                            </p>
                        </body>
                    </html>
                """

            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
            server.quit()
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

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Order Placed"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = instance.user.email
            to_email = instance.user.email

            html = """
                    <html>
                        <head></head>
                        <body>
                            Greetings """ + instance.user.username + """,
                            <br>
                            Your order has been prepared.
                            <p><b>Order Details</b></p>
                            <p>
                                <ul>
                                    <li><b>Order ID</b>: """ + order.id_string + """"</li>
                                    <li><b>Order placed on</b>: """ + order.created_at.strftime("%m/%d/%Y, %H:%M:%S") + """</li>
                                </ul>
                            </p>
                        </body>
                    </html>
                """

            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
            server.quit()

    except Exception as e:
        print(e)

    try:
        if instance._declined:
            restaurant = instance.cart.first().restaurant
            userrole = UserRole.objects.get(restaurant=restaurant)
            source_user = userrole.user
            description = "Your order '" + instance.id_string + "' has been declined."
            noti = Notification.objects.create(
                content_object=source_user,
                order=instance,
                title="Order Declined",
                destination_id=instance.user.pk,
                description=description
            )

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Order Placed"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = instance.user.email
            to_email = instance.user.email

            html = """
                <html>
                    <head></head>
                    <body>
                        Greetings """ + instance.user.username + """,
                        <br>
                        Your order has been declined by """ + restaurant.name + """.
                        <p><b>Order Details</b></p>
                        <p>
                            <ul>
                                <li><b>Order ID</b>: """ + order.id_string + """"</li>
                                <li><b>Order placed on</b>: """ + order.created_at.strftime("%m/%d/%Y, %H:%M:%S") + """</li>
                            </ul>
                        </p>
                    </body>
                </html>
            """

            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
            server.quit()
    except Exception as e:
        pass


post_save.connect(order_event_notification, sender=Order)
