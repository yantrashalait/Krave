from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ValidatingPasswordChangeForm
from django.urls import reverse_lazy, reverse


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/index.php'


class RestaurantDetailView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/rest_detail.php'


class RestaurantEditView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/rest_detail.php'


class OrderView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'restaurant/orders.php'


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