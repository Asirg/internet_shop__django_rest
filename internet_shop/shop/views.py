from django.db import models

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Product, Comment, ProductCategory
from shop.serializers import ProductDetailSerializer, ProductListSerializer, CommentCreateSerializer, ReviewCreateSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer
from shop.service import ProductFilter

# Create your views here.

class ProductListView(generics.ListAPIView):

    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter

    def get_queryset(self):
        products = Product.objects.all().annotate(
            review_user = models.Count("reviews", filter=models.Q(reviews__user = self.request.user))
        ).annotate(
            avg_rating = models.Sum(models.F("reviews__rating")) / models.Count(models.F("reviews"))
        ).annotate(
            quantity_review = models.Count(models.F("reviews"))
        )
        return products

class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = (DjangoFilterBackend, )

class ProductCategoryDetailView(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)