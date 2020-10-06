from django.db.models import Count, Sum

from core.models import FoodMenu, Restaurant, RestaurantRating, FoodRating, FoodCart, Order


def get_restaurant_rating(restaurant_id):
    ratings = RestaurantRating.objects.filter(restaurant_id=restaurant_id)
    if not ratings:
        return 4.3
    else:
        avg_rating = round((sum(ratings) / len(ratings)), 1)
        return avg_rating


def sort_restaurants_by_ratings(restaurant_value):
    return sorted(restaurant_value, key=lambda x: x[1], reverse=True)


def popular_restaurants():
    restaurants = Restaurant.objects.filter(hidden=False)
    restaurant_ratings = [(restaurant.name, get_restaurant_rating(restaurant.id)) for restaurant in restaurants]
    sorted_by_ratings = sort_restaurants_by_ratings(restaurant_ratings)
    sorted_restaurants = [rest_tuple[0] for rest_tuple in sorted_by_ratings]
    return sorted_restaurants


def trending_foods():
    foods = FoodMenu.objects.all().annotate(
        number_in_carts=Count('cart__number_of_food')
    ).order_by('-number_in_carts')
    return foods
