from django.core.exceptions import PermissionDenied
from userrole.models import UserRole
from core.models import Restaurant

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class RestaurantAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        restaurant_id = kwargs.pop('rest_id')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            if request.user.is_authenticated:
                if request.role.group.name == 'restaurant-owner':
                    if UserRole.objects.filter(user=request.user, restaurant=restaurant).exists():
                        return super(RestaurantAdminMixin, self).dispatch(request, *args, **kwargs)
        except Restaurant.DoesNotExist:
            pass
        raise PermissionDenied()