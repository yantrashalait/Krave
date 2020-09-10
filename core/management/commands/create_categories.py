from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from core.models import Category

User = get_user_model()


class Command(BaseCommand):
    help = "create categories"

    def handle(self, *args, **kwargs):
        categories = [
            'Breakfast',
            'Lunch',
            'Dinner',
        ]
        for category in categories:
            user = User.objects.filter(is_superuser=True)[0]
            category, _created = Category.objects.get_or_create(created_by=user, name=category)
            category.created_by = user
            category.save()
            self.stdout.write(self.style.SUCCESS('Category {} created'.format(category)))
