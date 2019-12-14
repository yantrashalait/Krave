from django.contrib import admin
from .models import Restaurant, RestaurantRequest, Restaurant, FoodMenu, FoodCustomize, RestaurantCuisine, \
    RestaurantFoodCategory
import django.contrib.gis.admin as gisadmin

class RestaurantRequestAdmin(gisadmin.OSMGeoAdmin):
    modifiable = True

admin.site.register(RestaurantRequest, RestaurantRequestAdmin)


class RestaurantCuisineInline(admin.TabularInline):
    model = RestaurantCuisine

class RestaurantCategoryInline(admin.TabularInline):
    model = RestaurantFoodCategory

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [RestaurantCuisineInline, RestaurantCategoryInline]

class FoodCustmomizeInline(admin.TabularInline):
    model = FoodCustomize


class FoodMenuAdmin(admin.ModelAdmin):
    inlines = [FoodCustmomizeInline, ]

admin.site.register(FoodMenu, FoodMenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)