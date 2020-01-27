from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.db.models import Sum
from django.core.validators import validate_email
import re
from .models import RestaurantRequest, FoodMenu, FoodCustomize, RestaurantFoodCategory

from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
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

        if User.objects.filter(email=email_of_owner, is_restaurant=True).exists():
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
    calories = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Calories'}))

    def __init__(self, *args, **kwargs):
        super(FoodMenuForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'fd-ct'})

    class Meta:
        model = FoodMenu
        fields = ('category', 'name', 'description', 'ingredients', 'old_price', 'new_price', 'preparation_time', 'image', 'calories', 'image')


class  FoodMenuModifierForm(forms.ModelForm):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'fd-ct'}), choices=((1, "Optional"), (2, "Required")))

    def __init__(self, *args, **kwargs):
        super(FoodMenuModifierForm, self).__init__(*args, **kwargs)
        self.fields['name_of_ingredient'].required = False
        self.fields['cost_of_addition'].required = False

    class Meta:
        model = FoodCustomize
        fields = ('name_of_ingredient', 'cost_of_addition', 'calories', 'type')

