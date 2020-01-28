from django.contrib.auth.forms import PasswordChangeForm
import re
from django.core.exceptions import ValidationError
from django import forms
from core.models import Restaurant
from django.contrib.gis import forms as gisforms

class ValidatingPasswordChangeForm(PasswordChangeForm):
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


