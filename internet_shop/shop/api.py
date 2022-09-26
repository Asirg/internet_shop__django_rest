from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import ProductCategory
from shop.serializers import ProductCategorySerializer, ProductCategoryDetailSerializer

class ProductCategoryViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend, )

    def list(self, request):
        queryset = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, url=None):
        queryset = ProductCategory.objects.all()
        category = get_object_or_404(queryset, url=url)
        serializer = ProductCategoryDetailSerializer(category)
        return Response(serializer.data)

