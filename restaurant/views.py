import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from .permissions import RestaurantAdminMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers

from core.views import randomString
from delivery.tasks import assign_delivery
from .forms import ValidatingPasswordChangeForm
from core.models import Order, FoodMenu, FoodStyle, FoodExtra, Restaurant, RestaurantCuisine, \
Cuisine, RestaurantFoodCategory, FoodCart, RestaurantPayment, RestaurantImage
from core.forms import FoodMenuForm, FoodMenuStyleForm, FoodMenuExtraForm, RestaurantForm, \
RestaurantCategoryForm, RestaurantEditForm

StyleFormSet = inlineformset_factory(FoodMenu, FoodStyle, form=FoodMenuStyleForm, fields=['name_of_style', 'cost',], extra=1, max_num=10)
ExtraFormSet = inlineformset_factory(FoodMenu, FoodExtra, form=FoodMenuExtraForm, fields=['name_of_extra', 'cost'], extra=1, max_num=10)


# new dashboard
class DashboardView(RestaurantAdminMixin, TemplateView):
    template_name = 'restaurant/dashboard.html'


class RestaurantDetailView(RestaurantAdminMixin, UpdateView):
    template_name = 'restaurant/restaurant_detail.html'
    form_class = RestaurantForm
    model = Restaurant

    def get_object(self):
        id_ = self.kwargs.get('rest_id')
        return get_object_or_404(Restaurant, pk=id_)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
        context['cuisine'] = Cuisine.objects.all()
        context['categories'] = RestaurantFoodCategory.objects.filter(restaurant=self.request.restaurant)
        try:
            context['rest_cuisine'] = RestaurantCuisine.objects.get(restaurant=self.request.restaurant)
        except RestaurantCuisine.DoesNotExist:
            pass
        return context


class RestaurantEditDetailView(RestaurantAdminMixin, UpdateView):
    template_name = 'restaurant/restaurant_detail_edit.html'
    form_class = RestaurantEditForm
    model = Restaurant

    def get_object(self):
        id_ = self.kwargs.get('rest_id')
        return get_object_or_404(Restaurant, pk=id_)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantEditDetailView, self).get_context_data(*args, **kwargs)
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

        # un-hide the restaurant if restaurant email is inserted.
        if self.object.email != "" or self.object.email != " " or self.object.email is not None:
            self.object.hidden = False
        else:
            self.object.hidden = True
        self.object.save()
        if 'cuisines[]' in self.request.POST:
            rest_cuisine, created = RestaurantCuisine.objects.get_or_create(restaurant=self.object)
            for item in self.request.POST.getlist('cuisines[]'):
                id_ = int(item)
                cuisine = Cuisine.objects.get(id=id_)
                if not cuisine in rest_cuisine.cuisine.all():
                    rest_cuisine.cuisine.add(cuisine)
            rest_cuisine.save()

        if 'image' in self.request.FILES:
            restaurant_image = self.request.FILES['image']
            if not RestaurantImage.objects.filter(restaurant=self.object):
                RestaurantImage.objects.create(restaurant=self.object, image=restaurant_image, main_image=True)
            else:
                rest_img = RestaurantImage.objects.get(restaurant=self.object)
                rest_img.image = restaurant_image
                rest_img.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id})


class OrderView(RestaurantAdminMixin, ListView):
    login_url = 'login'
    model = Order
    # template_name = 'restaurant/orders.php'
    template_name = 'restaurant/web_order.html'
    context_object_name = 'orders'

    def get_queryset(self, *args, **kwargs):
        # return self.model.objects.filter(Q(paid=True)|Q(payment=1), cart__restaurant=self.request.restaurant, status=1).order_by('-added_date')
        return self.model.objects.all()


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
    # template_name = 'restaurant/food-items.php'
    template_name = 'restaurant/food_list.html'
    context_object_name = 'foods'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant_id=self.kwargs.get('rest_id'))


class MenuEditView(RestaurantAdminMixin, UpdateView):
    model = FoodMenu
    # template_name = 'restaurant/index.php'
    template_name = 'restaurant/add_food_item.html'
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
    template_name = 'restaurant/food_confirm_delete.html'

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


class MenuAddView(RestaurantAdminMixin, CreateView):
    model = FoodMenu
    template_name = 'restaurant/add_food_item.html'
    form_class = FoodMenuForm

    def get_context_data(self, *args, **kwargs):
        context = super(MenuAddView, self).get_context_data(**kwargs)
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
        kwargs = super(MenuAddView, self).get_form_kwargs(*args, **kwargs)
        kwargs['restaurant'] = self.request.restaurant
        return kwargs


# crud for restaurant food categories
class CategoryListView(RestaurantAdminMixin, ListView):
    login_url = 'login'
    model = RestaurantFoodCategory
    template_name = 'restaurant/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.request.restaurant)


class CategoryEditView(RestaurantAdminMixin, UpdateView):
    login_url = 'login'
    model = RestaurantFoodCategory
    template_name = 'restaurant/category_add.html'
    form_class = RestaurantCategoryForm

    def get_object(self):
        id_ = self.kwargs.get('category_id')
        return get_object_or_404(RestaurantFoodCategory, pk=id_)

    def get_success_url(self):
        return reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id})


class CategoryDeleteView(RestaurantAdminMixin, DeleteView):
    login_url = 'login'
    model = RestaurantFoodCategory
    template_name = 'restaurant/restaurantfoodcategory-confirm-delete.html'

    def get_object(self):
        id_ = self.kwargs.get('category_id')
        return get_object_or_404(RestaurantFoodCategory, pk=id_)

    def get_success_url(self):
        return reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id})

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
            return render(request, 'restaurant/restaurantfoodcategory-confirm-delete.php', {'message': error})

        return HttpResponseRedirect(success_url)


class CategoryCreateView(RestaurantAdminMixin, CreateView):
    login_url = 'login'
    template_name = 'restaurant/category_add.html'
    form_class = RestaurantCategoryForm
    model = RestaurantFoodCategory

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.restaurant = self.request.restaurant
            self.object.save()

            return HttpResponseRedirect(reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id}))

    def get_success_url(self):
        return reverse('restaurant:category-list', kwargs={'rest_id': self.request.restaurant.id})


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


def change_order_status(request, *args, **kwargs):
    if request.method == 'POST':
        order = Order.objects.get(id=kwargs.get('order_id'))
        status = request.POST.get('status_id')
        order.status = status
        # order._prepared = False
        # order._runsignal = False
        # order._approved = True
        order.save()

    return JsonResponse({'success': True})


def accept_order(request, *args, **kwargs):
    try:
        order = Order.objects.get(id=kwargs.get('order_id'))
        order.status = 2
        order._prepared = False
        order._runsignal = False
        order._approved = True
        order.save()
    except Order.DoesNotExist:
        pass

    return redirect(reverse_lazy('restaurant:order', kwargs={'rest_id': request.restaurant.id}))


def decline_order(request, *args, **kwargs):
    try:
        order = Order.objects.get(id=kwargs.get('order_id'))
        order.status = 3
        order._prepared = False
        order._runsignal = False
        order._approved = False
        order._declined = True
        order.save()
    except Order.DoesNotExist:
        pass
    return redirect(reverse_lazy('restaurant:order', kwargs={'rest_id': request.restaurant.id}))


def ready_order(request, *args, **kwargs):
    order = Order.objects.get(id=kwargs.get('order_id'))
    order.status = 4
    order._prepared = True
    order._runsignal = False
    order._approved = False
    order.save()
    restaurant_found, delivery_assigned = assign_delivery(order.pk, order.cart.first().restaurant.pk)
    if not restaurant_found:
        print('No restaurant has been found')
    if not delivery_assigned:
        print('Delivery has not been assigned')
    return redirect(reverse_lazy('restaurant:accepted-order', kwargs={'rest_id': request.restaurant.id}))


def manual_order(request, *args, **kwargs):
    if request.method == "GET":
        foods = FoodMenu.objects.filter(restaurant=request.restaurant.id, deleted=False)
        cart = FoodCart.objects.filter(session_key=request.session.session_key, checked_out=False)

        return render(request, 'restaurant/rest_order.html', {'foods': foods, 'carts': cart})

    if request.method == "POST":
        food_id = int(request.POST.get('food'))
        food = FoodMenu.objects.get(id=food_id)

        restaurant = request.restaurant
        qty = request.POST.get('qty', 1)

        if not request.session.session_key:
            request.session.save()

        cart = FoodCart.objects.create(food=food, session_key=request.session.session_key, number_of_food=qty, restaurant=restaurant)

        if 'extras' in request.POST:
            extras = request.POST.getlist('extras')
            for item in extras:
                try:
                    extra = FoodExtra.objects.get(name_of_extra=item.replace("_", " "), food=food)
                except:
                    extra = FoodExtra.objects.filter(name_of_extra=item.replace("_", " "), food=food)[0]
                cart.extras.add(extra)

        if 'radio3' in request.POST:
            try:
                style = FoodStyle.objects.get(
                    name_of_style=request.POST.get('radio3', '').replace("_", " "), food=food)
            except:
                style = FoodStyle.objects.filter(
                    name_of_style=request.POST.get('radio3', '').replace("_", ""), food=food)[0]
            cart.style = style
        cart.save()

        return HttpResponseRedirect(reverse('restaurant:manual-order'))


class FoodCartListView(ListView):
    template_name = 'restaurant/checkout.php'
    model = FoodCart
    context_object_name = "carts"

    def get_queryset(self):
        return self.model.objects.filter(session_key=self.request.session.session_key, checked_out=False)


class FoodCartDeleteView(DeleteView):
    model = FoodCart
    template_name = "restaurant/foodcart_confirm_delete.php"

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(FoodCart, pk=id_)

    def get_success_url(self):
        return reverse('restaurant:food-cart')


def add_to_order(request, *args, **kwargs):
    if request.method == "GET":
        return render(request, "restaurant/order.php")
    if request.method == "POST":
        order = Order()
        cart = FoodCart.objects.filter(session_key=request.session.session_key, checked_out=False)
        total = 0
        for item in cart:
            total += item.get_total
            restaurant = item.restaurant

        total += restaurant.delivery_charge
        order.total_price = total
        order.paid = False

        first_name = request.POST.get("first_name", "")
        middle_name = request.POST.get("middle_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        contact_number = request.POST.get("contact", "")

        address_line1 = request.POST.get("address1", "")
        address_line2 = request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip = request.POST.get("zip", "")

        order.first_name = first_name
        order.last_name = last_name
        order.middle_name = middle_name
        order.email = email
        order.contact_number = contact_number
        order.address_line1 = address_line1
        order.address_line2 = address_line2
        order.city = city
        order.state = state
        order.zip_code = zip

        if 'comment' in request.POST:
            message = request.POST.get('comment', '')
            order.note = message

        order.payment = 1

        last_order = Order.objects.last()
        if last_order:
            order_id = last_order.id
            order_id = order_id + 1

        else:
            order_id = 1

        id_string = randomString() + str(order_id)
        if Order.objects.filter(id_string=id_string).exists():
            id_string = randomString() + str(order_id)
            order.id_string = id_string
        else:
            order.id_string = id_string

        order.status = 1
        order._runsignal = False
        order._approved = False
        order._prepared = False
        order.save()

        for item in cart:
            order.cart.add(item)
            item.checked_out = True
            item.save()
        order._runsignal = False
        order._approved = False
        order._prepared = False
        order.save()

        return HttpResponseRedirect('/')


class PaymentListView(ListView):
    model = RestaurantPayment
    template_name = "restaurant/my_payment.html"
    context_object_name = "earnings"

    def get_queryset(self, *args, **kwargs):
        return RestaurantPayment.objects.filter(restaurant=self.request.restaurant)


class PaymentListSearchView(ListView):
    model = RestaurantPayment
    template_name = "restaurant/my_payment.html"
    context_object_name = "earnings"

    def get_queryset(self, *args, **kwargs):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            return RestaurantPayment.objects.filter(date__range=[start_date, end_date])


def list_chef_special(request):
    object_list = FoodMenu.objects.filter(chef_special=True, restaurant=request.restaurant)
    return render(request, 'restaurant/chef_special.html', {'object_list': object_list})


def add_chef_special(request):
    if request.method == "POST":
        food_id = int(request.POST.get('food'), 0)
        food = FoodMenu.objects.filter(id=food_id).update(chef_special=True)
        return HttpResponseRedirect(reverse('restaurant:chef-special'))
    else:
        foods = FoodMenu.objects.filter(restaurant=request.restaurant)
        return render(request, 'restaurant/chef_special_add.html', {'foods': foods})


def delete_chef_special(request, pk):
    food = FoodMenu.objects.get(id=pk)
    food.chef_special = False
    food.save()
    return HttpResponseRedirect(reverse('restaurant:chef-special'))
