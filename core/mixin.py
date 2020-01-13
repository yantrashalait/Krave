from django.contrib.auth.decorators import login_required, user_passes_test
from userrole.models import UserRole
from django.core.exceptions import PermissionDenied


user_login_required = user_passes_test(lambda user: user.is_superuser, login_url='/')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class SuperAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not UserRole.objects.filter(user=request.user, group__name="super-admin"):
            raise PermissionDenied()
        return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)


def is_super_admin(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func
