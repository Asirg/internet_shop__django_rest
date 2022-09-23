from django.db import models

from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Product, Comment, ProductCategory
from shop.serializers import ProductDetailSerializer, ProductListSerializer, CommentSerializer, ReviewCreateSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer
from shop.service import ProductFilter, PaginationProducts

# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    pagination_class = PaginationProducts

    def get_queryset(self):
        products = Product.objects.all().annotate(
            review_user = models.Count("reviews", filter=models.Q(reviews__user_id = self.request.user.id))
        ).annotate(
            avg_rating = models.Sum(models.F("reviews__rating")) / models.Count(models.F("reviews"))
        ).annotate(
            quantity_review = models.Count(models.F("reviews"))
        )
        return products

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer

class ReviewCreateViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    


# class ProductListView(generics.ListAPIView):

#     serializer_class = ProductListSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = ProductFilter

#     def get_queryset(self):
#         products = Product.objects.all().annotate(
#             review_user = models.Count("reviews", filter=models.Q(reviews__user = self.request.user))
#         ).annotate(
#             avg_rating = models.Sum(models.F("reviews__rating")) / models.Count(models.F("reviews"))
#         ).annotate(
#             quantity_review = models.Count(models.F("reviews"))
#         )
#         return products

# class ProductCategoryListView(generics.ListAPIView):
#     queryset = ProductCategory.objects.all()
#     serializer_class = ProductCategorySerializer
#     filter_backends = (DjangoFilterBackend, )

# class ProductCategoryDetailView(generics.RetrieveAPIView):
#     queryset = ProductCategory.objects.all()
#     serializer_class = ProductCategoryDetailSerializer

# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer

# class ReviewCreateView(generics.CreateAPIView):
#     serializer_class = ReviewCreateSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class CommentCreateView(generics.CreateAPIView):
#     serializer_class = CommentCreateSerializer
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)