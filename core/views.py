from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from .models import RestaurantRequest, Restaurant, FoodMenu, RestaurantImage, FoodCart, FoodCustomize, Order
from django.conf import settings
from userrole.models import UserRole
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .mixin import LoginRequiredMixin, SuperAdminMixin, is_super_admin

from .forms import LoginForm, SignUpForm, RestaurantRequestForm

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import transaction
from django.db.models import Sum


from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .signup_tokens import account_activation_token
from django.conf import settings
from .forms import RestaurantRequestForm
from user.models import UserProfile

from user.forms import ValidatingPasswordChangeForm
from django.contrib import messages

import random
import string


def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    character = ''.join(random.choice(letters) for i in range(stringLength))
    character = 'O' + character
    return character


def restaurant_register(request, *args, **kwargs):
    if request.method == 'GET':
        form = RestaurantRequestForm()
        return render(request, 'core/add_resturent.html', {'form': form})

    if request.method == 'POST':
        form = RestaurantRequestForm(request.POST)
        if form.is_valid():
            print('valid chaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            form.save()
        else:
            print('not valid')
            return render(request, 'core/add_resturent.html', {'form': form})
        return HttpResponseRedirect('/')


class RequestList(SuperAdminMixin, ListView):
    template_name = 'core/restaurantrequests.html'
    model = RestaurantRequest
    context_object_name = 'req'

    def get_queryset(self, *args, **kwargs):
        return RestaurantRequest.objects.filter(accepted=False, rejected=False)


class RequestDetail(SuperAdminMixin, DetailView):
    template_name = 'core/restaurantrequest_detail.html'
    model = RestaurantRequest
    context_object_name = 'req'


@is_super_admin
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

    # create restaurant object
    name = req.name
    contact = req.contact
    street = req.street
    town = req.town
    state = req.state
    zip_code = req.zip_code
    owner = req.name_of_owner
    registration_number = req.registration_number

    restaurant, created = Restaurant.objects.get_or_create(
        name=name, 
        contact=contact,
        owner=owner,
        registration_number=registration_number,
        street=street,
        town=town,
        state=state,
        zip_code=zip_code)

    group = Group.objects.get(name='restaurant-owner')
    userrole = UserRole.objects.create(user=user, group=group, restaurant=restaurant)
    user.groups.add(group)
    print('Successfully created')

    mail_subject = 'Restaurant Registered.'
    current_site = get_current_site(request)
    message = render_to_string('core/restaurant_registration_success_email.html', {
        'name': name,
        'domain': settings.SITE_URL,
        'username': username,
        'owner': owner,
        'password': password,
    })

    to_email = email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()    

    return HttpResponseRedirect('/requests/')


@is_super_admin
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

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['foods'] = FoodMenu.objects.order_by('-created_date')[:10]
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='restaurant-owner').exists():
                return HttpResponseRedirect(reverse('restaurant:dashboard', kwargs={'rest_id': self.request.restaurant.id}))
            else:
                return render(self.request, self.template_name, context=self.get_context_data())
        else:
            return render(self.request, self.template_name, context=self.get_context_data())


class RestaurantDetail(TemplateView):
    template_name = 'core/restaurant__detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        name = self.kwargs.get('rest_name').replace('_', ' ')
        restaurant = Restaurant.objects.get(name=name)
        context['restaurant'] = restaurant
        context['main_image'] = RestaurantImage.objects.filter(restaurant=restaurant, main_image=True)[0:1]
        return context


class RestaurantListView(ListView):
    template_name = 'core/restaurant__list.html'
    model = Restaurant
    context_object_name = 'restaurants'

    def get_queryset(self):
        try:
            name = self.request.GET['name']
        except:
            name = ''
        if name != '':
            object_list = self.model.objects.filter(name__icontains=name)
        else:
            object_list = self.model.objects.all()
        
        return object_list


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
        food = FoodMenu.objects.get(pk=request.GET.get('food_id'))
        customization = food.customizes.all()
        food = serializers.serialize('json', [food])
        customization = serializers.serialize('json', customization)
        data = {'food': food, 'modifiers': customization}
        return JsonResponse(data, safe=False)


"""
    This view is to display all the foods in a page
"""
class FoodListView(ListView):
    template_name = 'core/food_listing.html'
    model = FoodMenu
    context_object_name = 'foods'

    def get_queryset(self):
        try:
            name = self.request.GET['name']
        except:
            name = ""
        if name != "":
            object_list = self.model.objects.filter(name__icontains=name)
        else:
            object_list = self.model.objects.all()
        
        return object_list


class FoodCartListView(LoginRequiredMixin, ListView):
    template_name = 'core/checkout.html'
    model = FoodCart
    context_object_name = 'lists'

    def get_queryset(self):
        print(self.model.objects.filter(user=self.request.user, checked_out=False))
        return self.model.objects.filter(user=self.request.user, checked_out=False)


def web_authenticate(username=None, password=None):
    try:
        if "@" in username:
            user = User.objects.get(email__iexact=username)
        else:
            user = User.objects.get(username__iexact=username)
        if user.check_password(password):
            return authenticate(username=user.username, password=password), False
        else:
            return None, True  # Email is correct
    except User.DoesNotExist:
        return None, False  # false Email incorrect


def signin(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user, valid_email = web_authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('core:dashboard'))
                else:
                    return render(request, 'core/login.html',
                                  {'form': form,
                                   'email_error': "Your Account is Deactivated, Please Contact Administrator.",
                                   'valid_email': valid_email,
                                   'login_username': username
                                   })
            else:
                if valid_email:
                    email_error = False
                    password_error = True
                else:
                    password_error = False
                    email_error = "Invalid Username, please check your username."
                return render(request, 'core/login.html',
                              {'form': form,
                               'valid_email': valid_email,
                               'email_error': email_error,
                               'password_error': password_error,
                               'login_username': username
                               })
        else:
            if request.POST.get('login_username') is not None:
                login_username = request.POST.get('login_username')
            else:
                login_username = ''
            return render(request, 'core/login.html', {
                'form': form,
                'valid_email': False,
                'email_error': "Your username and password did not match.",
                'login_username': login_username
            })
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form, 'valid_email': True, 'email_error': False})


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            # save user role
            group = Group.objects.get(name='customer')
            UserRole.objects.get_or_create(user=user, group=group)

            # save user profile
            UserProfile.objects.get_or_create(user=user)

            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('core/acc_active_email.html', {
                'user': user,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'core/emailnotify.html', {'email': user.email})

        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            return render(request, 'core/register.html', {
                'form': form,
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'valid_email': True,
                'email_error': False
            })
    else:
        form = SignUpForm()
        return render(request, 'core/register.html', {
            'form': form,
            'valid_email': True,
            'email_error': False
        })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return redirect(reverse_lazy('login'))
    else:
        return HttpResponse('Activation link is invalid!')


"""
    View to add foods to order then proceed to cart
"""
@login_required(login_url='/login/')
@transaction.atomic
def add_to_order(request, *args, **kwargs):
    if request.method == 'POST':
        if 'food_identifier' in request.POST:        
            if 'qty' in request.POST:
                if int(request.POST.get('qty', 0)) < 1:
                    print('Items are less than 1') # here handle exception

                quantity = request.POST.get('qty', 1)
                food_id = int(request.POST.get('food_identifier'))
                food = FoodMenu.objects.get(id=food_id)

                restaurant = Restaurant.objects.get(id=food.restaurant.id)

                # uncomment the following line to check if the user is placing foods to cart from
                # different restaurants
                if FoodCart.objects.filter(user=request.user).count() > 0:
                    if FoodCart.objects.filter(~Q(restaurant=restaurant), checked_out=False).exists():
                        return render(request, 'core/message.html', {'message': 'You have already ordered food from another restaurant. To place order from another restaurant, you need to checkout the first order.'})

                cart = FoodCart.objects.create(food=food, user=request.user, number_of_food=quantity, restaurant=restaurant)

                if 'optional_modifiers' in request.POST:
                    opt_modifiers = request.POST.getlist('optional_modifiers')
                    for item in opt_modifiers:
                        modifier = FoodCustomize.objects.get(name_of_ingredient=item, food=food)
                        cart.modifier.add(modifier)
                
                if 'radio3' in request.POST:
                    modifier = FoodCustomize.objects.get(name_of_ingredient=request.POST.get('radio3', None), food=food)
                    cart.modifier.add(modifier)
                cart.save()
            
        return HttpResponseRedirect(reverse('core:food-cart')) 


"""
place order
"""
@login_required(login_url='/login/')
@transaction.atomic
def place_order(request, *args, **kwargs):
    if request.method == "POST":
        order = Order()
        order.user = request.user
        order.status = 0
        order.payment = 1
        order.location_text = ''
        total = 0
        for item in FoodCart.objects.filter(user=request.user, checked_out=False):
            total += item.get_total
            restaurant = item.restaurant

        total += restaurant.delivery_charge
        order.total_price = total

        if 'comment' in request.POST:
            message = request.POST.get('comment', '')
            order.note = message
        last_order = Order.objects.last()
        if last_order:
            order_id = Order.objects.last().id
            order_id = order_id + 1
        else:
            order_id = 1
        id_string = randomString() + str(order_id)
        if Order.objects.filter(id_string=id_string).exists():
            id_string = randomString + str(order_id)
            order.id_string = id_string
        else:
            order.id_string = id_string
        order.save()
        for item in FoodCart.objects.filter(user=request.user, checked_out=False):
            order.cart.add(item)
            item.checked_out = True
            item.save()
        order.save()

        

    return HttpResponseRedirect('/')        