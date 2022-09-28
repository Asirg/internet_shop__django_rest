from dataclasses import field
from rest_framework import serializers

from shop import models

###################### VIEW
######### Common
#########

class ForeignKeyImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ProductImage
        fields = ("image", )

class FilterNestedListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        print(data)
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

#########
#########   ProductCategory
######### 

class ProductCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    children = RecursiveSerializer(many=True)

    class Meta:
        model = models.ProductCategory

        list_serializer_class = FilterNestedListSerializer

        fields = ("name", "url", "image", "children")
        
    
class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = models.ProductCategory

        fields= "__all__" #("name", "image", )

#########
######### Product
#########

class ProductListSerializer(serializers.ModelSerializer):
    """Вывод списка товаров"""

    review_user = serializers.BooleanField()
    avg_rating = serializers.IntegerField()
    quantity_review = serializers.IntegerField()
    images = ForeignKeyImageSerializer(many=True)

    categories = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    # categories = CategorySerializer(many=True)

    class Meta:
        model = models.Product
        fields = ("name", "description", "cost", "categories", "review_user", "avg_rating", "quantity_review", "id", "images")



class CommentShowSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterNestedListSerializer
        model = models.Comment
        
        exclude = ("user", "product", "parent")

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        
        exclude = ("user", "product", "id",  )


class ProductDetailSerializer(serializers.ModelSerializer):

    review_user = serializers.BooleanField()
    avg_rating = serializers.IntegerField()
    quantity_review = serializers.IntegerField()

    # categories = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    categories = ProductCategoryDetailSerializer(read_only=True, many=True)
    
    comments = CommentShowSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ("id", "name", "description", "cost", "categories", "quantity", "reviews", "comments", "review_user", "avg_rating", "quantity_review",
            'childrens',
        )

###################### CREATE

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        exclude = ("user", )

    def create(self, validated_data):
        review, _ = models.Review.objects.update_or_create(
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

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ("content", "product", "parent")

    def update(self, instance, validated_data):
        print(instance)
        instance.content = validated_data.get("content")
        instance.save()
        return instance