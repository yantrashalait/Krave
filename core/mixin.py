from django.contrib.auth.decorators import login_required, user_passes_test
from userrole.models import UserRole
from django.core.exceptions import PermissionDenied


super_user_login_required = user_passes_test(lambda user: user.is_superuser, login_url='/')

def support_or_admin_check(user):
    return user.groups.filter(name="support").exists() or user.groups.filter(name="super-admin").exists()

support_or_admin_login_required = user_passes_test(support_or_admin_check)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class SuperAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="super-admin").exists():
            raise PermissionDenied()
        return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)


class StaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="super-admin").exists() and not request.user.groups.filter(name="support").exists():
            raise PermissionDenied()
        return super(StaffMixin, self).dispatch(request, *args, **kwargs) 


def is_super_admin(view_func):
    decorated_view_func = login_required(super_user_login_required(view_func))
    return decorated_view_func


def is_support_or_admin(view_func):
    decorated_view_func = login_required(support_or_admin_login_required(view_func))
    return decorated_view_func
