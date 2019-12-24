from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'is_restaurant', 'is_customer', 'is_deliveryman')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError('Password must contain alphabet characters, special characters and numbers')

        return password1


class ValidatingPasswordResetForm(auth.forms.SetPasswordForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError('Password must contain alphabet characters, special characters and numbers')

        return password1

