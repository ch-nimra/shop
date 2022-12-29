from django.contrib.auth.models import User
from django.db import models
from shop.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')

    

