from django.template import Library
from core.models import FoodMenu

register = Library()

@register.filter
def space_to_underscore(obj):
    return obj.replace(" ", "_")


@register.filter
def get_food_items(obj, rest):
    return FoodMenu.objects.filter(category=obj, restaurant=rest)