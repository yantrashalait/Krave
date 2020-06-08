from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from .models import Delivery, DeliveryTrack
from user.models import UserLocationTrack
from core.models import Order, Restaurant

User = get_user_model()
logger = get_task_logger(__name__)

# return True/False, True/False corresponding to 'Restaurant location not found', 'No user available' respectively.
@task(name="assign_delivery")
def assign_delivery(order_id, restaurant_id):
    logger.info('Assign delivery to a delivery person')
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        logger.info("No restaurant exists with id " + str(restaurant_id))
        return False, False
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.info("No order exists of specified id " + str(order_id))
        return False, False

    restaurant_location = restaurant.location_point
    if not restaurant_location:
        logger.info("The restaurant does not contain any location. id: " + str(restaurant_id))
        return False, False

    else:
        # if there exists a user near the restaurant that is available to delivery
        if User.objects.filter(is_deliveryman=True, is_available=True).exists():
            user_locations = UserLocationTrack.location_manager.near(longitude=restaurant.longitude, latitude=restaurant.latitude)
            user = user_locations[0].user
            Delivery.objects.create(order=order, delivery_man=user, tracking_code=order.id_string, status=0)
            logger.info("Delivery person assigned to order")
            return True, True
        # if no user is available
        else:
            logger.info("No user is available for delivery")
            return True, False
