from django.forms import ModelForm
from .models import Contact

from django import forms



class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class DateForm(forms.Form):
    start   = forms.DateField()
    end     = forms.DateField()