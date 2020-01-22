from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ValidatingPasswordChangeForm
from django.urls import reverse_lazy, reverse
from core.models import Order, Restaurant 
from django.http import HttpResponseRedirect


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/index.php'


class RestaurantDetailView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/rest_detail.php'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail'] = Restaurant.objects.get(id=self.kwargs.get("rest_id"))
        return context

def edit_restaurant(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name')
        town = request.POST.get('town')
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
        rest_qs.town = town
        rest_qs.contact = contact
        rest_qs.opening_time = opening_time
        rest_qs.closing_time = closing_time
        rest_qs.delivery_charge = delivery_charge
        rest_qs.registration_number = registration_number
        rest_qs.email = email
        if logo != None:
            rest_qs.logo = logo
        rest_qs.delivery_time = delivery_time
        rest_qs.save()
        
    return HttpResponseRedirect(reverse('restaurant:restaurant-detail', kwargs={'rest_id':request.restaurant.id}))



class RestaurantEditView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/rest_detail.php'


class OrderView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/orders.php'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(cart__restaurant=self.request.restaurant, status=0)
        return context


class AcceptedOrderView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/accepted-orders.php'


class MenuListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/food-items.php'


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


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_required = 'login'
    template_name = 'restaurant/orders_detail.php'
    model = Order
    context_object_name = 'order'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Order, id=self.kwargs.get('order_id'))