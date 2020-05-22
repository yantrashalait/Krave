from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Group

from userrole.models import UserRole
from core.models import Restaurant


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class SuperAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        super_group = Group.objects.get(name="super-admin")
        if UserRole.objects.filter(user=request.user, group=super_group).exists():
            return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()
