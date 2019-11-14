from django.core.management.base import BaseCommand, CommandError
from core.models import MealType


class Command(BaseCommand):
    help = 'create colors'

    def handle(self, *args, **kwargs):
        meals = ['Breakfast', 'Brunch', 'Elevenses', 'Supper', 'Lunch', 'Dinner']

        for meal in meals:
            MealType.objects.create(name=meal)
        print('Created meal types')