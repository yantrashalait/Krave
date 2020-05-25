from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from userrole.models import UserRole
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Assign users to customer'

    def handle(self, *args, **options):
        users = User.objects.filter(user_roles__group__name="customer")
        group = Group.objects.get(name='customer')
        for user in users:
            if not user.groups.filter(name="customer").exists():
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS("Assigned user {} to group customer".format(user)))
            self.stdout.write(self.style.SUCCESS("User {} already assigned to group customer".format(user)))
