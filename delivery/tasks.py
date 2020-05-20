from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from .models import Delivery, DeliveryTrack
from user.models import UserLocationTrack

User = get_user_model()
logger = get_task_logger(__name__)

# return True/False, True/False corresponding to 'Restaurant location not found', 'No user available' respectively.
@task(name="assign_delivery")
def assign_delivery(order, restaurant):
    logger.info('Assign delivery to a delivery boy')
    restaurant_location = restaurant.location_point
    if not restaurant_location:
        return False, None

    else:
        if User.objects.filter(is_deliveryman=True, is_available=True).exists():
            user_locations = UserLocationTrack.objects.distance(restaurant_location).filter(user__is_available=True).select_related('user').order_by('last_location_point')
            print(user_locations)
        else:
            return True, False
