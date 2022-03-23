from django.contrib import admin
from .models import instrument, cpc, Contact

admin.site.register(instrument)
admin.site.register(Contact)