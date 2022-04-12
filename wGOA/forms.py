from django.forms import ModelForm
from .models import Contact
from django.contrib.admin.widgets import AdminDateWidget
from django import forms

from django.core.validators import RegexValidator
numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')

CPC_YEAR_CHOICES = ['2014', '2015', '2016','2017', '2018', '2019', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029'] #add years here

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class DateForm(forms.Form):
    start   = forms.DateField(widget=forms.SelectDateWidget(years=CPC_YEAR_CHOICES),)
    # test2 = forms.DateField(widget =  AdminDateWidget)
    # start   = forms.IntegerField()
    # end     = forms.IntegerField()

    # https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
    # https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    # https://www.youtube.com/watch?v=I2-JYxnSiB0