from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .permissions import SuperAdminMixin
from django.contrib.auth import get_user_model

from core.models import Restaurant, RestaurantPayment, Order

User = get_user_model()


class HomeView(TemplateView):
    template_name = "dashboard/index.php"
    permission_classes = [SuperAdminMixin, ]


class RestaurantListView(ListView):
    template_name = "dashboard/restaurant-list.php"
    permission_classes = [SuperAdminMixin, ]
    queryset = Restaurant.objects.all()
    context_object_name = "restaurants"


class RestaurantDetailView(DetailView):
    template_name = "dashboard/restaurant-detail.php"
    permission_classes = [SuperAdminMixin, ]
    context_object_name = "restaurant"
    model = Restaurant


class RestaurantPaymentView(ListView):
    template_name = "dashboard/restaurant-payment.php"
    permission_classes = [SuperAdminMixin, ]
    model = RestaurantPayment
    context_object_name = "earnings"

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.kwargs.get('pk'))
