from django.contrib import admin
from .models import Restaurant, RestaurantRequest
import django.contrib.gis.admin as gisadmin

admin.site.register(Restaurant)

class RestaurantRequestAdmin(gisadmin.OSMGeoAdmin):
    modifiable = True

admin.site.register(RestaurantRequest, RestaurantRequestAdmin)