from django.core.exceptions import PermissionDenied
from userrole.models import UserRole
from core.models import Restaurant


class RestaurantAdminMixin(object):

    def dispatch(self, request, *args, **kwargs):
        restaurant_id = kwargs.pop('rest_id')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            if request.user.is_authenticated:
                if request.role.group.name == 'restaurant-owner':
                    if UserRole.objects.filter(user=request.user, restaurant=restaurant).exists():
                        return super(RestaurantAdminMixin, self).dispatch(request, *args, **kwargs)
        except:
            raise PermissionDenied()
        raise PermissionDenied()