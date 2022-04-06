from django.forms import ModelForm
from .models import Contact

from django import forms

from django.core.validators import RegexValidator
numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class DateForm(forms.Form):
    start   = forms.IntegerField()
    end     = forms.IntegerField()

    # https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
    # https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    # https://www.youtube.com/watch?v=I2-JYxnSiB0