from itertools import product
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TypeComment(models.Model):
    name = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100)

class Characteristic(models.Model):
    name = models.CharField(max_length=100)
    name_show = models.CharField(max_length=150)
    url = models.SlugField(unique=True)

    have_scroll = models.BooleanField()
    value_show = models.BooleanField()
    multirow = models.BooleanField()
    aggregation = models.BooleanField()

    def __str__(self) -> str:
        return self.name

class СharacteristicValue(models.Model):
    characteristic = models.ForeignKey(
        to=Characteristic, on_delete=models.CASCADE, verbose_name="Характеристика"
    )

    value = models.CharField(max_length=100)
    value_show = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.value} ({self.value_show})"

class GroupCharacteristics(models.Model):
    name = models.CharField(max_length=100)

    characteristics = models.ManyToManyField(
        to=Characteristic, related_name="group_characteristics"

    )

    def __str__(self) -> str:
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(unique=True)

    parent = models.ForeignKey(
        to = "self", on_delete=models.SET_NULL, null=True,
    )
    type_comment = models.ForeignKey(
        to=TypeComment, null=True, blank=True, on_delete=models.SET_NULL
    )

    classification_characteristics = models.ManyToManyField(
        to=Characteristic, blank=True
    )
    groups_characteristics = models.ManyToManyField(
        to=GroupCharacteristics, blank=True
    )

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.FloatField()

    categories = models.ManyToManyField(
        to=ProductCategory, related_name="product_categories"
    )

    @property
    def quantity(self):
        return 1
    # seller = models.ForeignKey(
    #     to=Seller, on_delete=models.CASCADE, related_name="product_seller"
    # )

class MaterialProduct(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE,
    )

    description = models.TextField()
    quantity = models.PositiveIntegerField()
    characteristic_value = models.ForeignKey(
        to=СharacteristicValue, on_delete=models.CASCADE, null=True, blank=True,
    )
    # stock = models.ForeignKey(
    #     to=
    # )

class ProductСharacteristic(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, null=True
    )
    characteristic = models.ForeignKey(
        to=Characteristic, on_delete=models.CASCADE, null=False
    )
    value = models.CharField(max_length=300)

class Comment(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE
    )

    user_name = models.CharField(max_length=100)
    positive = models.CharField(max_length=200)
    negative = models.CharField(max_length=200)
    content = models.TextField()
    raiting = models.PositiveSmallIntegerField()

class CommentPhoto(models.Model):
    image = models.ImageField(upload_to="comment_image/")
    comment_id = models.UUIDField(primary_key=False)

class ProductPhoto(models.Model):
    image = models.ImageField(upload_to="product_image/")

    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE,
    )
    characteristic_value = models.ForeignKey(
        to=СharacteristicValue, on_delete=models.CASCADE, null=True, blank=True,
    )