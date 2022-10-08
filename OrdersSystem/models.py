from django.db import models
from django.conf import settings


class Product(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=500)
    ProductImage = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=500, null=True)
    ProductPrice = models.BigIntegerField()
    Users = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True)
    class Meta:
        db_table = "Products"

# class User(models.Model):
#     UserId = models.AutoField(primary_key=True)
#     Username = models.CharField(max_length=500)
#     Products = models.ManyToManyField(Product)
#     class Meta:
#         db_table = "Users"