from cgitb import lookup
from dataclasses import field
from django_filters import rest_framework as filters

from shop.models import Product

class CharFilterInFIlter(filters.BaseInFilter, filters.CharFilter):
    pass

class ProductFilter(filters.FilterSet):
    categories = CharFilterInFIlter(field_name="categories__name", lookup_expr="in")
    cost = filters.RangeFilter()
    
    class Meta:
        model = Product
        fields = ['categories', 'cost', ]