from django.contrib import admin
from .models import Restaurant, RestaurantRequest, Restaurant, FoodMenu, FoodCustomize, RestaurantCuisine, \
    RestaurantFoodCategory, RestaurantImage, FoodCart, Order
import django.contrib.gis.admin as gisadmin

class RestaurantRequestAdmin(gisadmin.OSMGeoAdmin):
    modifiable = True

admin.site.register(RestaurantRequest, RestaurantRequestAdmin)


class RestaurantCuisineInline(admin.TabularInline):
    model = RestaurantCuisine

class RestaurantCategoryInline(admin.TabularInline):
    model = RestaurantFoodCategory

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [RestaurantCuisineInline, RestaurantCategoryInline, RestaurantImageInline]

class FoodCustmomizeInline(admin.TabularInline):
    model = FoodCustomize


class FoodMenuAdmin(admin.ModelAdmin):
    inlines = [FoodCustmomizeInline, ]

admin.site.register(FoodMenu, FoodMenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(FoodCart)
admin.site.register(Order)