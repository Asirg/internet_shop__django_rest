from importlib.metadata import SelectableGroups
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from shop.models import Product

class PaginationProducts(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "count": self.page.paginator.count,
            "result": data
        })


class CharFilterInFIlter(filters.BaseInFilter, filters.CharFilter):
    pass

class ProductFilter(filters.FilterSet):
    categories = CharFilterInFIlter(field_name="categories__name", lookup_expr="in")
    cost = filters.RangeFilter()
    
    class Meta:
        model = Product
        fields = ['categories', 'cost', ]