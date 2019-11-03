from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import RestaurantRequest, Restaurant
from django.conf import settings
from userrole.models import UserRole
from django.contrib.auth.models import Group
from user.models import User
from django.db import transaction
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect

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