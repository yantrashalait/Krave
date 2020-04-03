from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, TemplateView, CreateView, DeleteView
from .models import RestaurantRequest, Restaurant, FoodMenu, RestaurantImage, FoodCart, FoodExtra, FoodStyle, Order
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
from django.db.models import Sum, Max


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

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from decimal import Decimal

import random
import string

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
            form.save()
        else:
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

    domain = settings.SITE_URL
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Restaurant Registered"
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = email

    html = """
        <html>
            <head></head>
            <body>
                <p>Hi """ + owner + """,</p>
                <p>
                    Your request for registering your restaurant has been successful.

                    Your login credentials are:
                    <ul>
                        <li>username: """+ username + """</li>
                        <li>password: """+ password + """</li>
                    </ul>

                    <b>Please change the password after logging into your account for security purposes.</b>
                </p>

                <p>Kindly login to the system by clicking the following link:</p>
                """+ domain + """/login/.
            </body>
        </html>
    """

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)

    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
    server.quit()

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
                if not self.request.restaurant.email:
                    return HttpResponseRedirect(reverse('restaurant:restaurant-detail', kwargs={'rest_id': self.request.restaurant.id}))
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
        restaurant = food.restaurant
        styles = food.styles.all()
        extras = food.extras.all()
        restaurant = serializers.serialize('json', [restaurant])
        food = serializers.serialize('json', [food])
        styles = serializers.serialize('json', styles)
        extras = serializers.serialize('json', extras)
        data = {'food': food, 'styles': styles, 'extras': extras, 'restaurant': restaurant}
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


class FoodCartListView(ListView):
    template_name = 'core/checkout.html'
    model = FoodCart
    context_object_name = 'lists'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user, checked_out=False)
        else:
            return self.model.objects.filter(session_key=self.request.session.session_key, checked_out=False)

    def get_context_data(self, *args, **kwargs):
        context = super(FoodCartListView, self).get_context_data(**kwargs)
        max_time = self.get_queryset().aggregate(max_time=Max('food__preparation_time'))
        if self.get_queryset():
            delivery_time = self.get_queryset()[0].restaurant.delivery_time
            context['total_time'] = max_time['max_time'] + delivery_time
        return context

class FoodCartDeleteView(DeleteView):
    model = FoodCart

    def get_object(self):
        id_ = self.kwargs.get('cart_id')
        return get_object_or_404(FoodCart, pk=id_)

    def get_success_url(self):
        if not self.request.user.is_authenticated:
            return reverse('core:food-cart')
        else:
            return reverse('core:food-cart', kwargs={'username': self.request.user.username})

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
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
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
                    if FoodCart.objects.filter(session_key=session_key, checked_out=False, user=None).exists():
                        FoodCart.objects.filter(session_key=session_key, checked_out=False, user=None).update(user=user)
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

            to_email = email
            domain = settings.SITE_URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Activate Account"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = to_email

            html = """
                <html>
                    <head></head>
                    <body>
                        Hi """+ user.username +""",
                        Please click on the link to confirm your registration,
                        """ + domain + """/activate/"""+ uid +"""/"""+ token +"""/
                    </body>
                </html>
            """

            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
            server.quit()

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
        if not request.user.is_authenticated:
            if 'food_identifier' in request.POST:
                if int(request.POST.get('qty', 1)) < 1:
                    quantity = 1
                else:
                    quantity = request.POST.get('qty', 1)
                food_id = int(request.POST.get('food_identifier'))
                food = FoodMenu.objects.get(id=food_id)

                restaurant = Restaurant.objects.get(id=food.restaurant.id)
                if not request.session.session_key:
                    request.session.save()

                cart = FoodCart.objects.create(food=food, session_key=request.session.session_key, number_of_food=quantity, restaurant=restaurant)

                if 'extras' in request.POST:
                    extras = request.POST.getlist('extras')
                    for item in extras:
                        extra = FoodExtra.objects.get(name_of_extra=item.replace("_", " "), food=food)
                        cart.extras.add(extra)

                if 'radio3' in request.POST:
                    style = FoodStyle.objects.get(name_of_style=request.POST.get('radio3', None).replace("_", " "), food=food)
                    cart.style = style

                cart.save()
        else:
            if 'food_identifier' in request.POST:
                if 'qty' in request.POST:
                    if int(request.POST.get('qty', 0)) < 1:
                        return render(request, 'core/message.html', {'message': 'Items are less than 1.'})

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

                    if 'extras' in request.POST:
                        extras = request.POST.getlist('extras')
                        for item in extras:
                            extra = FoodExtra.objects.get(name_of_extra=item.replace("_", " "), food=food)
                            cart.extras.add(extra)

                    if 'radio3' in request.POST:
                        style = FoodStyle.objects.get(name_of_style=request.POST.get('radio3', None).replace("_", " "), food=food)
                        cart.style = style
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
        total = 0
        for item in FoodCart.objects.filter(user=request.user, checked_out=False):
            total += item.get_total
            restaurant = item.restaurant

        total += restaurant.delivery_charge
        order.total_price = total
        order.paid = False

        if 'comment' in request.POST:
            message = request.POST.get('comment', '')
            order.note = message

        order.address1 = request.POST.get('address1', '')
        order.address2 = request.POST.get('address2', '')
        order.city = request.POST.get('city', '')
        order.state = request.POST.get('state', '')
        order.zip_code = request.POST.get('zip', '')

        if request.POST.get('payment') == 'cod':
            order.payment = 1
        elif request.POST.get('payment') == 'paypal':
            order.payment = 2
        else:
            order.payment = 1

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

        order.status = 1
        order._runsignal = False
        order.save()
        for item in FoodCart.objects.filter(user=request.user, checked_out=False):
            order.cart.add(item)
            item.checked_out = True
            item.save()

        if order.payment == 2:
            request.session['order_id'] = order.id
            return redirect('core:process-payment')

        order._runsignal = True
        order.save()
    return HttpResponseRedirect('/')


def process_payment(request, *args, **kwargs):
    key = settings.STRIPE_PUBLISHABLE_KEY
    _id = request.session.get('order_id')
    return render(request, 'core/process_payment.html', {'key': key, 'id': _id})

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
def charge(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST['order-id'])
        try:
            order = Order.objects.get(id=int(request.POST.get('order-id', '')))
            if order.payment == 1:
                return render(request, 'core/payment_cancelled.html')
            elif order.paid == True:
                return render(request, 'core/payment_cancelled.html')
            else:
                charge = stripe.Charge.create(
                    amount=500,
                    currency='usd',
                    description='A django charge',
                    source=request.POST['stripeToken']
                )
                order.paid = True
                order._runsignal = True
                order.save()

                return render(request, 'core/payment_done.html')
        except Order.DoesNotExist:
            return render(request, 'core/payment_cancelled.html')



    else:
        return render(request, 'core/payment_done.html')
