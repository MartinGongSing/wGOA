from .models import instrument
import django_filters

class instrumFilter(django_filters.FilterSet):

    class Meta:
        model : instrument
        fields = ('name')