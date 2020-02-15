from django.db import models
from django.contrib.gis.db.models import PointField
from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


"""
    Restaurant model stores the details about restaurant profile that is visible to the public.
"""
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location_point = PointField(geography=True, srid=4326, blank=True, null=True)
    street = models.CharField(max_length=500, default='')
    town = models.CharField(max_length=500, default='')
    state = models.CharField(max_length=500, default='')
    zip_code = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=20)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    delivery_upto = models.TextField(help_text="Where do you deliver?", null=True, blank=True)
    delivery_charge = models.FloatField(help_text="Delivery charges in dollars", null=True, blank=True)
    owner = models.CharField(max_length=500, null=True, blank=True)
    logo = models.ImageField(upload_to="restaurant/logo/", null=True, blank=True)
    registration_number = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=500, default="")
    joined_date = models.DateTimeField(default=datetime.now)
    delivery_time = models.CharField(default='', max_length=200)

    @property
    def longitude(self):
        if self.location_point:
            return self.location_point.x

    @property
    def latitude(self):
        if self.location_point:
            return self.location_point.y

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="restaurant/")
    main_image = models.BooleanField(help_text="Make this your main image to be displayed?", default=False)

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RestaurantCuisine(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name="cuisines")
    cuisine = models.ManyToManyField(Cuisine)

    def __str__(self):
        return self.restaurant.name + ' '


"""
    This model stores the food categories
"""
class RestaurantFoodCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_category')
    category = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.category


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_review")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant_review')
    review = models.TextField()

    def __str__(self):
        return self.restaurant.name + ' ' + self.user.username


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant_rating")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant_rating')
    rating = models.IntegerField()

    def __str__(self):
        return self.restaurant.name + ' ' + self.user.username


"""
    It stores the detail about the food served by a specific restaurant.
"""
class FoodMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu")
    category = models.ForeignKey(RestaurantFoodCategory, on_delete=models.CASCADE, related_name="food")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField(null=True)
    old_price = models.FloatField()
    new_price = models.FloatField()
    # The preparation time of each food may vary according to the restaurant.
    preparation_time = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
    calories = models.FloatField(null=True, blank=True, help_text="calories contained in this food")
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if FoodCart.objects.filter(food__pk=self.pk).exists():
            raise Exception("Cannot delete food. This item is added in user's cart.")
        super(FoodMenu, self).delete(*args, **kwargs)


CUSTOMIZE_TYPE = (
    (1, 'optional'),
    (2, 'required')
)

class FoodStyle(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name="styles")
    name_of_style = models.CharField(max_length=255, help_text="Style that comes with this food.")
    cost = models.FloatField(help_text="Cost of style(in dollars)", null=True, blank=True)
    calories = models.CharField(max_length=100, null=True, blank=True, help_text="calories contained in this ingredient(in cal)")

    def __str__(self):
        return self.name_of_style


class FoodExtra(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name="extras")
    name_of_extra = models.CharField(max_length=255, help_text="Extra things that can come with the food")
    cost = models.FloatField(help_text="Cost of extras(in dollars)", null=True, blank=True)
    calories = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name_of_extra


class FoodReview(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name="food_review")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_review')
    review = models.TextField()

    def __str__(self):
        return self.food.name + ' ' + self.user.username


class FoodRating(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name="food_rating")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_rating')
    rating = models.IntegerField()

    def __str__(self):
        return self.food.name + ' ' + self.user.username


class RestaurantRequest(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=500, default='')
    town = models.CharField(max_length=500, default='')
    state = models.CharField(max_length=500, default='')
    zip_code = models.CharField(max_length=255, default='')
    name_of_owner = models.CharField(max_length=255)
    email_of_owner = models.EmailField()
    contact = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=255, help_text='registration number of restaurant')
    message = models.TextField(help_text="Explain in short why do you want to be registered here?")
    requested_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    does_your_restaurant_staff_deliver_order = models.BooleanField(blank=True, null=True)

    @property
    def longitude(self):
        if self.location:
            return self.location.x

    @property
    def latitude(self):
        if self.location:
            return self.location.y

    def __str__(self):
        return self.name


class FoodCart(models.Model):
    food = models.ForeignKey(FoodMenu, on_delete=models.DO_NOTHING, related_name='cart')
    number_of_food = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='cart')
    added_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    style = models.ForeignKey(FoodStyle, related_name='cart', on_delete=models.CASCADE, null=True, blank=True)
    extras = models.ManyToManyField(FoodExtra, related_name='cart')
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.food.name + ' ' + self.user.username

    @property
    def get_total(self):
        total = 0
        for item in self.extras.all():
            total += item.cost

        if self.style:
            total += self.style.cost * self.number_of_food
        else:
            total += self.food.new_price * self.number_of_food
        return total


class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Checked Out'),
        (2, 'Approved'),
        (3, 'Rejected'),
        (4, 'Prepared'),
        (5, 'Delivered')
    )

    PAYMENT_TYPE = (
        (1, 'On Delivery'),
    )

    cart = models.ManyToManyField(FoodCart, related_name="order")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='order')
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    payment = models.IntegerField(choices=PAYMENT_TYPE, null=True, blank=True)
    location_point = PointField(geography=True, srid=4326, blank=True, null=True)
    note = models.TextField(default='', null=True, blank=True)
    id_string = models.CharField(unique=True, default='', max_length=255)
    added_date = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(default=0)
    delivery_person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="deliveries", null=True, blank=True, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)

    address_line1 = models.CharField(max_length=255, default='')
    address_line2 = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip_code = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.user.username


class Notification(models.Model):
    source = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('source', 'object_id')
    destination = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    food = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    cart = models.ForeignKey(FoodCart, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
