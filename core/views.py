from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from .models import RestaurantRequest, Restaurant, FoodMenu, RestaurantImage, FoodCart, FoodCustomize
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
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse


from .forms import LoginForm, SignUpForm, RestaurantRequestForm

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db import transaction


from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .signup_tokens import account_activation_token
from django.conf import settings


class RestaurantRegister(TemplateView):
    template_name = 'core/add_resturent.html'


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

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['foods'] = FoodMenu.objects.order_by('-created_date')[:10]
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='restaurant-owner').exists():
                return HttpResponseRedirect(reverse('restaurant:dashboard'))
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
    template_name = 'core/restaurant_listing.html'
    model = Restaurant
    context_object_name = 'restaurants'


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
    queryset = FoodMenu.objects.all()
    context_object_name = 'foods'


"""
    Add foods to order
"""
def food_order_add(request, *args, **kwargs):
    pass


class FoodCartListView(TemplateView):
    template_name = 'core/checkout.html'


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
                    if user.groups.filter(name='restaurant-owner'):
                        return HttpResponseRedirect(reverse('restaurant:dashboard'))
                    else:
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
@transaction.atomic
def add_to_order(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.POST)
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
                # if FoodCart.objects.count() > 0:
                #     if FoodCart.objects.filter(~Q(restaurant=restaurant)).exists():
                #         pass

                cart, created = FoodCart.objects.get_or_create(
                    food=food, 
                    user=request.user, 
                    number_of_food=quantity, 
                    restaurant=restaurant)

                if 'optional_modifiers' in request.POST:
                    opt_modifiers = request.POST.getlist('optional_modifiers')
                    for item in opt_modifiers:
                        modifier = FoodCustomize.objects.get(name_of_ingredient=item, food=food)
                        cart.modifier.add(modifier)
                
                if 'radio3' in request.POST:
                    modifier = FoodCustomize.objects.get(name_of_ingredient=request.POST.get('radio3', None), food=food)
                    cart.modifier.add(modifier)
            
        return HttpResponseRedirect(reverse('core:food-cart')) 
            







