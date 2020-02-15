from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ValidatingPasswordChangeForm
from django.urls import reverse_lazy, reverse
from core.models import Order, FoodMenu, FoodStyle, FoodExtra, Restaurant, RestaurantCuisine, Cuisine, RestaurantFoodCategory
from core.forms import FoodMenuForm, FoodMenuStyleForm, FoodMenuExtraForm, RestaurantForm
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from .permissions import RestaurantAdminMixin
from django.contrib.gis.geos import Point
import json
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q


StyleFormSet = inlineformset_factory(FoodMenu, FoodStyle, form=FoodMenuStyleForm, fields=['name_of_style', 'cost',], extra=1, max_num=10)
ExtraFormSet = inlineformset_factory(FoodMenu, FoodExtra, form=FoodMenuExtraForm, fields=['name_of_extra', 'cost'], extra=1, max_num=10)

class DashboardView(RestaurantAdminMixin, CreateView):
    model = FoodMenu
    template_name = 'restaurant/index.php'
    form_class = FoodMenuForm

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['styleform'] = StyleFormSet(self.request.POST, prefix='styleform', instance=self.object)
            context['extraform'] = ExtraFormSet(self.request.POST, prefix='extraform', instance=self.object)

        else:
            context['styleform'] = StyleFormSet(prefix='styleform', instance=self.object)
            context['extraform'] = ExtraFormSet(prefix='extraform', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        styleform = context['styleform']
        extraform = context['extraform']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.restaurant = self.request.restaurant
            self.object.save()
            if styleform.is_valid() and extraform.is_valid():
                for form in styleform:
                    name_of_style = form.cleaned_data.get('name_of_style')
                    if name_of_style != '' and name_of_style != None and name_of_style != ' ':
                        print(name_of_style)
                        f = form.save(commit=False)
                        f.food = self.object
                        f.save()
                for form in extraform:
                    name_of_extra = form.cleaned_data.get('name_of_extra')
                    if name_of_extra != '' and name_of_extra != None and name_of_extra != ' ':
                        f = form.save(commit=False)
                        f.food = self.object
                        f.save()

                return HttpResponseRedirect(reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id}))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DashboardView, self).get_form_kwargs(*args, **kwargs)
        kwargs['restaurant'] = self.request.restaurant
        return kwargs


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
            rest_cuisine, created = RestaurantCuisine.objects.get_or_create(restaurant=self.object)
            for item in self.request.POST.getlist('cuisines[]'):
                id_ = int(item)
                cuisine =  Cuisine.objects.get(id=id_)
                if not cuisine in rest_cuisine.cuisine.all():
                    rest_cuisine.cuisine.add(cuisine)
            rest_cuisine.save()

        if 'categories' in self.request.POST:
            categories = self.request.POST.get('categories').replace(" ", "").split(',')
            for item in categories:
                RestaurantFoodCategory.objects.get_or_create(restaurant=self.object, category=item)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id})


class OrderView(RestaurantAdminMixin, ListView):
    login_url = 'login'
    model = Order
    template_name = 'restaurant/orders.php'
    context_object_name = 'orders'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(Q(paid=True)|Q(payment=1), cart__restaurant=self.request.restaurant, status=1)


class AcceptedOrderView(RestaurantAdminMixin, ListView):
    login_url = 'login'
    template_name = 'restaurant/accepted-orders.php'
    model = Order
    context_object_name = "orders"

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(cart__restaurant=self.request.restaurant, status=2)


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
            context['styleform'] = StyleFormSet(self.request.POST, prefix='styleform', instance=self.object)
            context['extraform'] = ExtraFormSet(self.request.POST, prefix='extraform', instance=self.object)

        else:
            context['styleform'] = StyleFormSet(prefix='styleform', instance=self.object)
            context['extraform'] = ExtraFormSet(prefix='extraform', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        styleform = context['styleform']
        extraform = context['extraform']
        self.object = form.save()

        with transaction.atomic():
            if styleform.is_valid() and extraform.is_valid():
                for form in styleform:
                    name_of_style = form.cleaned_data.get('name_of_style')
                    if name_of_style != '' and name_of_style != None and name_of_style != ' ':
                        print(name_of_style)
                        f = form.save(commit=False)
                        f.food = self.object
                        f.save()
                for form in extraform:
                    name_of_extra = form.cleaned_data.get('name_of_extra')
                    if name_of_extra != '' and name_of_extra != None and name_of_extra != ' ':
                        f = form.save(commit=False)
                        f.food = self.object
                        f.save()

                return HttpResponseRedirect(reverse('restaurant:menu-list', kwargs={'rest_id': self.request.restaurant.id}))

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MenuEditView, self).get_form_kwargs(*args, **kwargs)
        kwargs['restaurant'] = self.request.restaurant
        return kwargs

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

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except Exception as e:
            error = e
            return render(request, 'restaurant/food_confirm_delete.php', {'message': error})

        return HttpResponseRedirect(success_url)


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



def accept_order(request, *args, **kwargs):
    order = Order.objects.get(id=kwargs.get('order_id'))
    order.status = 2
    order._approved = True
    order.save()

    return redirect(reverse_lazy('restaurant:order', kwargs={'rest_id': request.restaurant.id}))
