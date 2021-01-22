from django_filters import rest_framework as filters

from .models import User


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class UserFilter(filters.FilterSet):
    view_id = NumberInFilter(field_name='view_id')
    role = NumberInFilter(field_name='role')

    class Meta:
        model = User
        fields = {'view_id': ['exact'],
                  'email': ['exact', 'iexact'],
                  'full_name': ['exact', 'iexact'],
                  'phone': ['exact', 'iexact'],
                  'role': ['exact'],
                  'created': ['exact'],
                  }
