from django.core.management.base import BaseCommand, CommandError
from core.models import Cuisine


class Command(BaseCommand):
    help = 'Create default cuisines'

    def handle(self, *args, **options):
        cuisine_list = [
            'Nepalese Cuisine',
            'Indian Cuisine', 
            'Italian Food',
            'Mexican Food',
            'Chinese Food',
            'Japanese Food',
            'Thai Cuisine',
            'French Cuisine',
            'American Food',
            'German Cuisine', 
            'Spanish Cuisine',
            'Seafood',
            'Vegetarian Food',
            'Russian Cuisine',
            'Turkish Food',
            'Sri Lankan Cuisine',
            'Korean Cuisine',
        ]
        for cuisine in cuisine_list:
            new_group, created = Cuisine.objects.get_or_create(name=cuisine)
            self.stdout.write('Successfully created cuisine .. "%s"' % cuisine)