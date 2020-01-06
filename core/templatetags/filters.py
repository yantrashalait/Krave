from django.template import Library
from core.models import FoodMenu

register = Library()

@register.filter
def space_to_underscore(obj):
    return obj.replace(" ", "_")


@register.filter
def get_food_items(obj, rest):
    return FoodMenu.objects.filter(category=obj, restaurant=rest)


@register.filter
def get_total_price(obj):
    total = 0
    for item in obj:
        total += item.get_total
    return total