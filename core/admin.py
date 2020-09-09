from django.contrib import admin
from .models import Restaurant, RestaurantRequest, Restaurant, FoodMenu, FoodStyle, FoodExtra, RestaurantCuisine, \
    RestaurantFoodCategory, RestaurantImage, FoodCart, Order, Cuisine, Category
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


class FoodStyleInline(admin.TabularInline):
    model = FoodStyle


class FoodExtraInline(admin.TabularInline):
    model = FoodExtra


class FoodMenuAdmin(admin.ModelAdmin):
    inlines = [FoodStyleInline, FoodExtraInline]


admin.site.register(RestaurantFoodCategory)
admin.site.register(Category)
admin.site.register(FoodMenu, FoodMenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(FoodCart)
admin.site.register(Order)
admin.site.register(RestaurantCuisine)
admin.site.register(Cuisine)
