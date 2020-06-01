import smtplib

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView, CreateView
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.models import Restaurant, RestaurantPayment, Order, RestaurantRequest
from core.mixin import SuperAdminMixin, is_super_admin, is_support_or_admin, StaffMixin
from userrole.models import UserRole
from user.models import UserProfile
from restaurant.forms import ValidatingPasswordChangeForm

User = get_user_model()


class HomeView(StaffMixin, TemplateView):
    template_name = "dashboard/index.php"


class RestaurantListView(StaffMixin, ListView):
    template_name = "dashboard/restaurant-list.php"
    queryset = Restaurant.objects.all()
    context_object_name = "restaurants"


class RestaurantDetailView(StaffMixin, DetailView):
    template_name = "dashboard/restaurant-detail.php"
    context_object_name = "restaurant"
    model = Restaurant


class RestaurantPaymentView(StaffMixin, ListView):
    template_name = "dashboard/restaurant-payment.php"
    model = RestaurantPayment
    context_object_name = "earnings"

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(restaurant=self.kwargs.get('pk'))


class RequestListView(StaffMixin, ListView):
    template_name = 'dashboard/restaurantrequests.php'
    model = RestaurantRequest
    context_object_name = 'req'

    def get_queryset(self, *args, **kwargs):
        return RestaurantRequest.objects.filter(accepted=False, rejected=False)


class RequestDetailView(StaffMixin, DetailView):
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


@is_support_or_admin
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
    server.sendmail(settings.EMAIL_HOST_USER, [email, ], msg.as_string())
    server.quit()

    return HttpResponseRedirect('/dashboard/requests/')


@is_support_or_admin
def decline_request(request, *args, **kwargs):
    req = RestaurantRequest.objects.get(id=kwargs.get('pk'))
    req.rejected = True
    req.save()
    return HttpResponseRedirect('/dashboard/requests/')


@is_support_or_admin
def change_password(request, *args, **kwargs):
    if request.method == "POST":
        form = ValidatingPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse_lazy('dashboard:restaurant-list'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ValidatingPasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.php',{'form': form})


class SupportStaffListView(SuperAdminMixin, ListView):
    model = User
    template_name = "dashboard/staff-list.php"
    queryset = User.objects.filter(user_roles__group__name="support")
    context_object_name = "staffs"


@is_super_admin
@transaction.atomic
def staff_create(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        contact = request.POST.get("contact", "")
        address = request.POST.get("address", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        image = request.FILES.get("image")

        if User.objects.filter(username=username).exists():
            context = {
                "username_error": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if User.objects.filter(email=email).exists():
            context = {
                "email_error": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not first_name or not last_name:
            context = {
                "name_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not email:
            context = {
                "email_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not username:
            context = {
                "username_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, image=image, address=address, contact=contact)

        group = Group.objects.get(name="support")
        UserRole.objects.create(user=user, group=group)
        user.groups.add(group)

        domain = settings.SITE_URL
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Login credentials for Mitho"
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = email

        html = """
            <html>
                <head></head>
                <body>
                    <p>Hi """ + first_name + """ """ + last_name + """,</p>
                    <p>
                        You have been registered into Mitho as a support user.

                        Your login credentials are:
                        <ul>
                            <li>username: """+ username + """</li>
                            <li>email: """+ email +"""</li>
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
        server.sendmail(settings.EMAIL_HOST_USER, [email, ], msg.as_string())
        server.quit()

        return HttpResponseRedirect('/dashboard/support/list/')
    else:
        return render(request, 'dashboard/staff-form.php')


class SupportStaffDetailView(SuperAdminMixin, DetailView):
    template_name = "dashboard/staff-detail.php"
    model = User
    context_object_name = "staff"


class DeliveryPersonListView(StaffMixin, ListView):
    template_name = "dashboard/staff-list.php"
    model = User
    context_object_name = "staffs"

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(user_roles__group__name="delivery")


@is_support_or_admin
def delivery_person_create(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        contact = request.POST.get("contact", "")
        address = request.POST.get("address", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        image = request.FILES.get("image")

        if User.objects.filter(username=username).exists():
            context = {
                "username_error": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if User.objects.filter(email=email).exists():
            context = {
                "email_error": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not first_name or not last_name:
            context = {
                "name_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not email:
            context = {
                "email_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        if not username:
            context = {
                "username_empty": True,
                "username": username,
                "email": email,
                "contact": contact,
                "address": address,
                "first_name": first_name,
                "last_name": last_name
            }
            return render(request, 'dashboard/staff-form.php', context)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        password = User.objects.make_random_password()
        user.set_password(password)
        user.is_deliveryman = True
        user.is_available = True
        user.save()

        UserProfile.objects.create(user=user, image=image, address=address, contact=contact)

        group = Group.objects.get(name="delivery")
        UserRole.objects.create(user=user, group=group)
        user.groups.add(group)

        domain = settings.SITE_URL
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Login credentials for Mitho"
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = email

        html = """
            <html>
                <head></head>
                <body>
                    <p>Hi """ + first_name + """ """ + last_name + """,</p>
                    <p>
                        You have been registered into Mitho as a delivery person.

                        Your login credentials are:
                        <ul>
                            <li>username: """+ username + """</li>
                            <li>email: """+ email +"""</li>
                            <li>password: """+ password + """</li>
                        </ul>

                        <b>Please change the password after logging into your account for security purposes.</b>
                    </p>
                </body>
            </html>
        """

        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, [email, ], msg.as_string())
        server.quit()

        return HttpResponseRedirect('/dashboard/delivery-person/list/')
    else:
        return render(request, 'dashboard/staff-form.php')
