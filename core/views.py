from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import RestaurantRequest, Restaurant, FoodMenu, RestaurantImage
from django.conf import settings
from userrole.models import UserRole
from django.contrib.auth.models import Group
from user.models import User
from django.db import transaction
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
from django.core import serializers
from django.db.models import Q


class RequestList(ListView):
    template_name = 'core/restaurantrequests.html'
    model = RestaurantRequest
    context_object_name = 'req'

    def get_queryset(self, *args, **kwargs):
        return RestaurantRequest.objects.filter(accepted=False, rejected=False)


class RequestDetail(DetailView):
    template_name = 'core/restaurantrequest_detail.html'
    model = RestaurantRequest
    context_object_name = 'req'

@transaction.atomic
def acceptRequest(request, *args, **kwargs):
    req = RestaurantRequest.objects.get(id=kwargs.get('pk'))
    req.accepted = True
    req.save()

    # create user from the provided information in the request 
    username = generate_username(req.name)
    password = User.objects.make_random_password()
    email = req.email_of_owner
    user = User.objects.create(username=username, email=email, is_restaurant=True)
    user.set_password(password)
    user.save()
    print(username)
    print(password)

    # create restaurant object
    name = req.name
    longitude = req.location.x
    latitude = req.location.y
    location = Point(longitude, latitude)
    contact = req.contact

    restaurant, created = Restaurant.objects.get_or_create(name=name, contact=contact)
    restaurant.location = location
    restaurant.save()
    

    group = Group.objects.get(name='restaurant-owner')
    userrole = UserRole.objects.create(user=user, group=group, restaurant=restaurant)
    print('Successfully created')

    return HttpResponseRedirect('/requests/')



def rejectRequest(request, *args, **kwargs):
    req = RestaurantRequest.objects.get(id=kwargs.get('pk'))
    req.rejected = True
    req.save()
    return HttpResponseRedirect('/requests/')


def generate_username(name):
    val = name.split(' ')[0].lower()
    x = 0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}".format(val, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 100000:
            raise Exception("Name is super popular")


class DashboardView(TemplateView):
    template_name = 'core/home.html'


class LoginView(TemplateView):
    template_name = 'core/login.html'


class RegisterView(TemplateView):
    template_name = 'core/register.html'


class RestaurantDetail(TemplateView):
    template_name = 'core/restaurant__detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        name = self.kwargs.get('rest_name').replace('_', ' ')
        restaurant = Restaurant.objects.get(name=name)
        context['restaurant'] = restaurant
        context['main_image'] = RestaurantImage.objects.filter(restaurant=restaurant, main_image=True)[0:1]
        return context


"""
    The search view
"""
def search(request, *args, **kwargs):
    if request.method == 'POST':
        food_menu = FoodMenu.objects.filter(Q(name__icontains=request.POST.get('search', '')) | Q(category__category__icontains=request.POST.get('search', '')))
        return render(request, 'core/search.html', {'foods': food_menu})
    
    else:
        return render(request, 'core/search.html')


"""
    This view is called by ajax request to get the detail of a food item
"""
def get_food_detail(request, *args, **kwargs):
    if request.method == 'GET':
        print(request.GET.get('food_id'))
        food = FoodMenu.objects.get(pk=request.GET.get('food_id'))
        food = serializers.serialize('json', [food])
        return JsonResponse(food, safe=False)


"""
    This view is to display all the foods in a page
"""
class FoodListView(ListView):
    template_name = 'core/food_listing.html'
    queryset = FoodMenu.objects.all()
    context_object_name = 'foods'




