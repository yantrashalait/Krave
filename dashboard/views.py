import smtplib

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.models import Restaurant, RestaurantPayment, Order, RestaurantRequest
from core.mixin import SuperAdminMixin, is_super_admin
from userrole.models import UserRole

User = get_user_model()


class HomeView(SuperAdminMixin, TemplateView):
    template_name = "dashboard/index.php"


class RestaurantListView(SuperAdminMixin, ListView):
    template_name = "dashboard/restaurant-list.php"
    queryset = Restaurant.objects.all()
    context_object_name = "restaurants"


class RestaurantDetailView(SuperAdminMixin, DetailView):
    template_name = "dashboard/restaurant-detail.php"
    context_object_name = "restaurant"
    model = Restaurant


class RestaurantPaymentView(SuperAdminMixin, ListView):
    template_name = "dashboard/restaurant-payment.php"
    model = RestaurantPayment
    context_object_name = "earnings"

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.kwargs.get('pk'))


class RequestListView(SuperAdminMixin, ListView):
    template_name = 'dashboard/restaurantrequests.php'
    model = RestaurantRequest
    context_object_name = 'req'

    def get_queryset(self, *args, **kwargs):
        return RestaurantRequest.objects.filter(accepted=False, rejected=False)


class RequestDetailView(SuperAdminMixin, DetailView):
    template_name = 'dashboard/restaurantrequest_detail.php'
    model = RestaurantRequest
    context_object_name = 'req'


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


@is_super_admin
@transaction.atomic
def accept_request(request, *args, **kwargs):
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

    return HttpResponseRedirect('/dashboard/requests/')


@is_super_admin
def decline_request(request, *args, **kwargs):
    req = RestaurantRequest.objects.get(id=kwargs.get('pk'))
    req.rejected = True
    req.save()
    return HttpResponseRedirect('/dashboard/requests/')
