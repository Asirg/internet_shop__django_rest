from dataclasses import field
from itertools import product
from pyexpat import model
from select import select
from rest_framework import serializers

from shop import models

###################### VIEW

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductCategory

        fields="__all__"
    
class ProductCategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductCategory

        fields="__all__"
        

class ProductListSerializer(serializers.ModelSerializer):
    """Вывод списка товаров"""

    review_user = serializers.BooleanField()
    avg_rating = serializers.IntegerField()
    quantity_review = serializers.IntegerField()

    categories = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    # categories = CategorySerializer(many=True)

    class Meta:
        model = models.Product
        fields = ("name", "description", "cost", "categories", "review_user", "avg_rating", "quantity_review")

class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = models.Comment
        
        exclude = ("user", "product", )

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        
        exclude = ("user", "product", "id",  )


class ProductDetailSerializer(serializers.ModelSerializer):

    # categories = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    categories = ProductCategoryDetailSerializer(read_only=True, many=True)
    
    comments = CommentSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ("name", "description", "cost", "categories", "quantity", "reviews", "comments"
        )

###################### CREATE

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        exclude = ("user", )

    def create(self, validated_data):
        review = models.Review.objects.update_or_create(
            user=validated_data.get("user", None),
            product=validated_data.get("product", None),
            defaults={
                "user_name":validated_data.get("user_name"),
                "positive":validated_data.get("positive"),
                "negative":validated_data.get("negative"),
                "content":validated_data.get("content"),
                "rating":validated_data.get("rating"),
            }
        )
        return review

class CommentCreateSerializer(serializers.ModelSerializer):

    # Должн быть валидация id и parent

    class Meta:
        model = models.Comment
        fields = ("content", "product",)

    def create(self, validated_data):
        comment = models.Comment.objects.filter(pk=validated_data.get("id", None))
        if comment:
            comment.update(content=validated_data.get("content"))
        else:
            comment = models.Comment.objects.create(
                user=validated_data.get("user"),
                product=validated_data.get("product"),
                parent_id=validated_data.get("parent", None),
                content=validated_data.get("content")
            )
        return comment

