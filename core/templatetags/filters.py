from django.template import Library
from core.models import FoodMenu
from datetime import datetime
from datetime import time

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


@register.filter
def is_past_time(opening_time, closing_time):
    current_time = datetime.now().time()
    if current_time < opening_time or current_time > closing_time:
        return True
    else:
        return False
