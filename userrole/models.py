from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from core.models import Restaurant

class UserRole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_roles', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_roles')
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE, related_name="user_roles")

    def __str__(self):
        return self.user.username + 'Roles'