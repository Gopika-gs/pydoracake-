from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Categorys(models.Model):

    img = models.ImageField(upload_to='pics')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
   

class Products(models.Model):
    img = models.ImageField(upload_to='pics')
    name = models.CharField( max_length=100)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE , null=True)
    price = models.IntegerField()

  
class CustomerCart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, blank=False)
    addedon = models.DateTimeField(auto_now_add=True)

class CustomerCheckout(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200,null=True,default = None)
    total_amount = models.FloatField()
    payment_signature = models.CharField(max_length=200,null=True,default = None)
    reciept_num = models.CharField(max_length=200)
    delivery_address =  models.CharField(max_length=2000)
    delivery_phone =  models.CharField(max_length=20)
    payment_complete = models.IntegerField(default = 0)
    payedon = models.DateTimeField(auto_now_add=True)

class customerPayedProducts(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    product_description = models.CharField(max_length=1000)
    checkout_details = models.ForeignKey(CustomerCheckout, on_delete=models.CASCADE, null=False, blank=False)