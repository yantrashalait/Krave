from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

class DashboardView(TemplateView):
    template_name = 'restaurant/index.php'


class RestaurantDetailView(TemplateView):
    template_name = 'restaurant/rest_detail.php'


class RestaurantEditView(TemplateView):
    template_name = 'restaurant/rest_detail.php'


class OrderView(TemplateView):
    template_name = 'restaurant/orders.php'


class AcceptedOrderView(TemplateView):
    template_name = 'restaurant/accepted-orders.php'


class MenuListView(TemplateView):
    template_name = 'restaurant/food-items.php'