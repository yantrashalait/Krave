from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.db.models import Sum
from django.core.validators import validate_email
import re
from .models import RestaurantRequest, FoodMenu, FoodStyle, FoodExtra, RestaurantFoodCategory, Restaurant, Category

from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
from django.contrib.gis import forms as gisforms
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.contrib.auth.tokens import PasswordResetTokenGenerator

default_token_generator = PasswordResetTokenGenerator()

User = get_user_model()


class RestaurantRequestForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'text__field__f', 'placeholder': 'Restaurant Name'}))
    name_of_owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'half_ _width__textform min__input__divider__first', 'placeholder': 'Name of Owner'}))
    email_of_owner = forms.CharField(widget=forms.EmailInput(attrs={'class': 'half_ _width__textform min__input__divider__sec', 'placeholder': 'Email'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'text__field__f', 'placeholder': 'Contact Number'}))
    registration_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'text__field__f', 'placeholder': 'Restaurant Registration Number'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea', 'placeholder': 'Leave a message'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'half__width__textform', 'placeholder': 'Street Name'}))
    town = forms.CharField(widget=forms.TextInput(attrs={'class': 'half__width__textform min__size', 'placeholder': 'Town Name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'half__width__textform', 'placeholder': 'State'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'half__width__textform min__size', 'placeholder': 'Zip Code'}))
    does_your_restaurant_staff_deliver_order = forms.ChoiceField(widget=forms.Select(attrs={'class': 'text__field__f', 'placeholder': 'Does your restaurant staff deliver orders?'}), choices=((None, 'Does your restaurant staff deliver orders?'),(0, 'No'), (1, 'Yes')))

    class Meta:
        model = RestaurantRequest
        fields = ('name', 'name_of_owner', 'email_of_owner', 'contact', 'registration_number', 'message', 'street', 'town', 'state', 'zip_code', 'does_your_restaurant_staff_deliver_order')

    def clean_email_of_owner(self):
        email_of_owner = self.cleaned_data.get('email_of_owner')
        if validate_email(email_of_owner) == False:
            raise ValidationError('Enter a valid Email address')

        if User.objects.filter(email=email_of_owner).exists():
            raise ValidationError('Restaurant with this email already exists')
        return email_of_owner


class LoginForm(forms.Form):
    username = forms.CharField(label='Your Email/Username', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100 )
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email address', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Your Password', max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput, label='One more time?', max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password1')
        password1 = self.cleaned_data.get('password2')
        if password != password1:
            raise ValidationError({'password1': ['The passwords did not match']})

        else:
            if password:
                if len(password) < 8:
                    raise ValidationError({'password1': ['Passwords must be of more than 8 characters']})

                pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
                if not bool(pattern.search(password)):
                    raise ValidationError(
                        {'password1': ['Password must contain alphabet characters, special characters and numbers']})

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email) == False:
            raise ValidationError('Enter a valid Email address')

        if User.objects.filter(email=email):
            raise ValidationError('User with this email already exists')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('User with this username already exists')
        else:
            return username


class FoodMenuForm(forms.ModelForm):
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'fd-ct'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Item Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Keep it more descriptive in less words'}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Separate with comma(,)'}))
    old_price = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Old Price'}))
    new_price = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New Price'}))
    preparation_time = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E.g. (10-20)'}))
    main_category = forms.ModelChoiceField(queryset=Category.objects.all())
    rest_category = forms.ModelChoiceField(queryset=RestaurantFoodCategory.objects.all())

    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant')
        super(FoodMenuForm, self).__init__(*args, **kwargs)
        self.fields['main_category'].widget.attrs.update({'class': 'fd-ct'})
        self.fields['rest_category'].widget.attrs.update({'class': 'fd-ct'})
        self.fields['rest_category'].queryset = RestaurantFoodCategory.objects.filter(restaurant=restaurant)

    class Meta:
        model = FoodMenu
        fields = (
            'main_category',
            'rest_category',
            'name',
            'description',
            'ingredients',
            'old_price',
            'new_price',
            'preparation_time',
            'image')


class FoodMenuStyleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuStyleForm, self).__init__(*args, **kwargs)
        self.fields['name_of_style'].required = False
        self.fields['cost'].required = False

    class Meta:
        model = FoodStyle
        fields = ('name_of_style', 'cost')


class FoodMenuExtraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuExtraForm, self).__init__(*args, **kwargs)
        self.fields['name_of_extra'].required = False
        self.fields['cost'].required = False

    class Meta:
        model = FoodExtra
        fields = ('name_of_extra', 'cost')


class RestaurantForm(forms.ModelForm):
    opening_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    closing_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Restaurant
        fields = ('name', 'location_point', 'street', 'town', 'state', 'zip_code', 'contact', 'opening_time', 'closing_time', 'delivery_upto', 'delivery_charge', 'logo', 'registration_number', 'email', 'delivery_time')

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        if not self.fields['location_point'].initial:
            self.fields['location_point'].initial = Point(-73.935242, 40.730610, srid=4326)
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['street'].widget.attrs['disabled'] = 'disabled'
        self.fields['town'].widget.attrs['disabled'] = 'disabled'
        self.fields['state'].widget.attrs['disabled'] = 'disabled'
        self.fields['zip_code'].widget.attrs['disabled'] = 'disabled'
        self.fields['contact'].widget.attrs['disabled'] = 'disabled'
        self.fields['delivery_upto'].widget.attrs['disabled'] = 'disabled'
        self.fields['delivery_charge'].widget.attrs['disabled'] = 'disabled'
        self.fields['registration_number'].widget.attrs['disabled'] = 'disabled'
        self.fields['email'].widget.attrs['disabled'] = 'disabled'
        self.fields['delivery_time'].widget.attrs['disabled'] = 'disabled'
        self.fields['opening_time'].widget.attrs['disabled'] = 'disabled'
        self.fields['closing_time'].widget.attrs['disabled'] = 'disabled'


class RestaurantEditForm(forms.ModelForm):
    opening_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    closing_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Restaurant
        fields = ('name', 'location_point', 'street', 'town', 'state', 'zip_code', 'contact', 'opening_time', 'closing_time', 'delivery_upto', 'delivery_charge', 'logo', 'registration_number', 'email', 'delivery_time')

    def __init__(self, *args, **kwargs):
        super(RestaurantEditForm, self).__init__(*args, **kwargs)
        if not self.fields['location_point'].initial:
            self.fields['location_point'].initial = Point(-73.935242, 40.730610, srid=4326)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name of restaurant'})
        self.fields['street'].widget.attrs.update({'placeholder': 'Street'})
        self.fields['town'].widget.attrs.update({'placeholder': 'Town'})
        self.fields['state'].widget.attrs.update({'placeholder': 'State'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Zip Code'})
        self.fields['contact'].widget.attrs.update({'placeholder': 'Contact Number'})
        self.fields['delivery_upto'].widget.attrs.update({'placeholder': 'Accepted delivery location upto...'})
        self.fields['delivery_charge'].widget.attrs.update({'placeholder': 'E.g. 4'})
        self.fields['registration_number'].widget.attrs.update({'placeholder': 'Restaurant registration number'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email of restaurant'})
        self.fields['delivery_time'].widget.attrs.update({'placeholder': 'E.g. 10-20(in minutes)'})


class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model = RestaurantFoodCategory
        fields = ('category', 'image')


class CustomPasswordResetForm(PasswordResetForm):
    def save(self, subject_template_name, html_email_template_name, email_template_name, from_email, use_https=True, domain_override=None, request=None,token_generator=default_token_generator, extra_email_context=None):
        to_email = request.POST['email']
        user = User.objects.get(email=request.POST['email'])

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "Password Reset"
        msg["From"] = settings.EMAIL_HOST_USER
        msg["To"] = to_email
        protocol = "https"
        domain = "krave.yantrashala.com"
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        site_name = "Krave"
        token = token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        html = """
            <html>
                <head></head>
                <body>
                    <p>You're receiving this email because you requested a
                    password reset for your user account at"""+ site_name +"""</p>

                    <p>Please go to the following page and choose a new password:</p><br>
                    """ + protocol + """://"""+ domain + url +"""
                    <br>
                    <p>
                    Your username, in case you've forgotten: """+ user.username +"""<br><br>

                    Thanks for using our site!

                    The """+ site_name +""" team
                    </p>
                </body>
            </html>
        """
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, [to_email, ], msg.as_string())
        server.quit()
