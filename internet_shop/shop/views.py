from math import prod
from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from shop.models import Product, Comment, ProductCategory
from shop.serializers import ProductDetailSerializer, ProductListSerializer, CommentCreateSerializer, ReviewCreateSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer

# Create your views here.

class ProductListView(APIView):
    def get(self, request):
        # products = Product.objects.all().annotate(
        #     comment_user = models.Case(
        #         models.When(comments__user = request.user, then=True),
        #         default=False,
        #         output_field=models.BooleanField(),
        #     ),
        # )
        products = Product.objects.all().annotate(
            review_user = models.Count("reviews", filter=models.Q(reviews__user = request.user))
        ).annotate(
            avg_rating = models.Sum(models.F("reviews__rating")) / models.Count(models.F("reviews"))
        ).annotate(
            quantity_review = models.Count(models.F("reviews"))
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductCategoryDetailView(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailSerializer


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

class ReviewCreateView(APIView):
    def post(self, request):
        Review = ReviewCreateSerializer(data=request.data)
        if Review.is_valid():
            Review.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)


class CommentCreateView(APIView):
    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save(
                user=request.user,
                id=request.data.get("id", None), 
                parent=request.data.get("parent", None))
            
            return Response(status=201)
        else:
            return Response(status=400)