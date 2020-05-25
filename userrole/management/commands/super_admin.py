from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from userrole.models import UserRole
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Assign user to super admin'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        user = User.objects.get(username=options.get('username'))
        group = Group.objects.get(name='super-admin')
        UserRole.objects.get_or_create(user=user, group=group)
        user.groups.add(group)
        self.stdout.write('Successfully created super admin')
