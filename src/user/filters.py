from django_filters import rest_framework
from django_filters.rest_framework import filters

from .models import User


class UserFilter(rest_framework.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='contains')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    registration_date = filters.DateFromToRangeFilter(field_name='registration_date')

    class Meta:
        model = User
        fields = ['email', 'name', 'is_verified', 'is_active', 'registration_date']
