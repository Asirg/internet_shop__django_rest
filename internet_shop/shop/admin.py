from django.contrib import admin

from shop.models import (TypeComment, Characteristic, СharacteristicValue, Comment, ReviewPhoto,Review, 
GroupCharacteristics, ProductCategory, Product, MaterialProduct, ProductСharacteristic, ProductPhoto)

admin.site.register(TypeComment)
admin.site.register(Characteristic)
admin.site.register(СharacteristicValue)
admin.site.register(GroupCharacteristics)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(MaterialProduct)
admin.site.register(ProductСharacteristic)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(ReviewPhoto)
admin.site.register(ProductPhoto)
# Register your models here.
