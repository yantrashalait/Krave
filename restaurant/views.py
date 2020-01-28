from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ValidatingPasswordChangeForm
from django.urls import reverse_lazy, reverse
from core.models import Order, FoodMenu, FoodCustomize, Restaurant, RestaurantCuisine, Cuisine
from core.forms import FoodMenuForm, FoodMenuModifierForm, RestaurantForm
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from .permissions import RestaurantAdminMixin
from django.contrib.gis.geos import Point
import json
from django.contrib.gis.geos import GEOSGeometry


ModifierImageFormset = inlineformset_factory(FoodMenu, FoodCustomize, form=FoodMenuModifierForm, fields=['name_of_ingredient', 'calories', 'cost_of_addition', 'type'], extra=1, max_num=10)

class DashboardView(RestaurantAdminMixin, CreateView):
    model = FoodMenu
    template_name = 'restaurant/index.php'
    form_class = FoodMenuForm

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['modifierform'] = ModifierImageFormset(self.request.POST, prefix='modifierform', instance=self.object)
        
        else:
            context['modifierform'] = ModifierImageFormset(prefix='modifierform', instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        modifierform = context['modifierform']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.restaurant = self.request.restaurant
            self.object.save()
            if modifierform.is_valid():
                for form in modifierform:
                    f = form.save(commit=False)
                    f.food = self.object
                    f.save()
                return HttpResponseRedirect('/restaurant/' + str(self.request.restaurant.id))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id})


class RestaurantDetailView(RestaurantAdminMixin, UpdateView):
    template_name = 'restaurant/rest_detail.php'
    form_class = RestaurantForm
    model = Restaurant

    def get_object(self):
        id_ = self.kwargs.get('rest_id')
        return get_object_or_404(Restaurant, pk=id_)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
        context['cuisine'] = Cuisine.objects.all()
        try:
            context['rest_cuisine'] = RestaurantCuisine.objects.get(restaurant=self.request.restaurant)
        except RestaurantCuisine.DoesNotExist:
            pass
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        longitude = float(self.request.POST.get('lon'))
        latitude = float(self.request.POST.get('lat'))

        location = Point(longitude, latitude)
        self.object.location_point = location
        self.object.save()
        if 'cuisines[]' in self.request.POST:
            rest_cuisine = RestaurantCuisine.objects.get(restaurant=self.object)
            for item in request.POST.getlist('cuisines[]'):
                id_ = int(item)
                cuisine =  Cuisine.objects.get(id=id_)
                if not cuisine in rest_cuisine.cuisine.all():
                    rest_cuisine.cuisine.add(cuisine)
            rest_cuisine.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id})



# class RestaurantDetailView(RestaurantAdminMixin, TemplateView):
#     login_url = 'login'
#     template_name = 'restaurant/rest_detail.php'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cuisine'] = Cuisine.objects.all()
#         context['form'] = RestaurantForm(restaurant=self.request.restaurant)
#         try:
#             context['rest_cuisine'] = RestaurantCuisine.objects.get(restaurant=self.request.restaurant)
#         except:
#             pass
#         return context
        

def edit_restaurant(request, *args, **kwargs):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        name = request.POST.get('name')
        street = request.POST.get('street')
        town = request.POST.get('town')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        contact = request.POST.get('contact')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        delivery_charge = request.POST.get('delivery_charge')
        registration_number = request.POST.get('registration_number')
        email = request.POST.get('email')
        logo = request.FILES.get('logo')
        delivery_time = request.POST.get('delivery_time')


        rest_qs = request.restaurant
        rest_qs.name = name
        rest_qs.street = street
        rest_qs.town = town
        rest_qs.state = state
        rest_qs.zip_code = zip_code
        rest_qs.contact = contact
        rest_qs.opening_time = opening_time
        rest_qs.closing_time = closing_time
        rest_qs.delivery_charge = delivery_charge
        rest_qs.registration_number = registration_number
        rest_qs.email = email
        if logo != None:
            rest_qs.logo = logo
        rest_qs.delivery_time = delivery_time
        
        if form.is_valid():
            print('asdsadsa')
            print(form.cleaned_data['location_point'])

        location = request.POST.get('location_point')
        location = location.replace(" ", "")[1:-2]
        coordinates_x = location.split(",")[1]
        coordinates_y = location.split(",")[2]
        longitude = coordinates_x.split(":[")[1]
        latitude = float(coordinates_y)
        longitude = float(longitude)
        # latitude = latitude / 100000
        # longitude = longitude / 100000
        # longitude = str(longitude)
        # latitude = str(latitude)
        # print(longitude, latitude)
        points = Point(longitude, latitude)
        print(points)

        location = GEOSGeometry('POINT(' + longitude + ' ' + latitude + ')')
        rest_qs.location_point = location
        rest_qs.save()

        rest_cuisine = RestaurantCuisine.objects.get(restaurant=rest_qs)
        for item in request.POST.getlist('cuisines[]'):
            id_ = int(item)
            cuisine =  Cuisine.objects.get(id=id_)
            if not cuisine in rest_cuisine.cuisine.all():
                rest_cuisine.cuisine.add(cuisine)
        rest_cuisine.save()        
    return HttpResponseRedirect(reverse('restaurant:restaurant-detail', kwargs={'rest_id':request.restaurant.id}))



class RestaurantEditView(RestaurantAdminMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/rest_detail.php'


class OrderView(RestaurantAdminMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/orders.php'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(cart__restaurant=self.request.restaurant, status=0)
        return context


class AcceptedOrderView(RestaurantAdminMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/accepted-orders.php'


class MenuListView(RestaurantAdminMixin, ListView):
    login_url = 'login'
    model = FoodMenu
    template_name = 'restaurant/food-items.php'
    context_object_name = 'foods'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant_id=self.kwargs.get('rest_id'))


class MenuEditView(RestaurantAdminMixin, UpdateView):
    model = FoodMenu
    template_name = 'restaurant/index.php'
    form_class = FoodMenuForm

    def get_object(self):
        id_ = self.kwargs.get('food_id')
        return get_object_or_404(FoodMenu, pk=id_)

    def get_context_data(self, *args, **kwargs):
        context = super(MenuEditView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['modifierform'] = ModifierImageFormset(self.request.POST, prefix='modifierform', instance=self.object)
        
        else:
            context['modifierform'] = ModifierImageFormset(prefix='modifierform', instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        modifierform = context['modifierform']
        self.object = form.save()

        with transaction.atomic():
            if modifierform.is_valid():
                for form in modifierform:
                    if form.cleaned_data.get('name_of_ingredient') != '':
                        f = form.save(commit=False)
                        f.food = self.object
                        f.save()
                        return HttpResponseRedirect(reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id}))
                    else:
                        return HttpResponseRedirect(reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id}))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id})


class MenuDeleteView(RestaurantAdminMixin, DeleteView):
    model = FoodMenu
    template_name = 'restaurant/food_confirm_delete.php'

    def get_object(self):
        id_ = self.kwargs.get('food_id')
        return get_object_or_404(FoodMenu, pk=id_)

    def get_success_url(self):
        return reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id})


@login_required
def change_password(request, *args, **kwargs):
    if request.method == "POST":
        form = ValidatingPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse_lazy('restaurant:dashboard', kwargs={'rest_id': request.restaurant.id}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ValidatingPasswordChangeForm(request.user)
    return render(request, 'restaurant/change_password.html',{'form': form})


class OrderDetailView(RestaurantAdminMixin, DetailView):
    login_required = 'login'
    template_name = 'restaurant/orders_detail.php'
    model = Order
    context_object_name = 'order'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Order, id=self.kwargs.get('order_id'))