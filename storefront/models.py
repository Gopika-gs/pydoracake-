import datetime
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
    flavour = models.CharField(max_length=100,default='chocolate')
    price = models.IntegerField()
    shape = models.CharField(max_length=50)
    size = models.IntegerField(default='6')
  
UPGRADE_CHOICES = (
    ('1/2kg','1/2kg'),
    ('1kg','1kg')
)   

CONTENT_CHOICES = (
    ('egg','egg'),
    ('eggless','eggless')
)  



class CustomerCart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, blank=False)
    price  = models.IntegerField(default=0,null=False)
    quantity = models.IntegerField(default=0)
    addedon = models.DateTimeField(auto_now_add=True)
    upgrade = models.CharField(choices=UPGRADE_CHOICES,default='1/2kg', max_length=10)
    content = models.CharField(choices=CONTENT_CHOICES,default='egg', max_length=10)
    message = models.CharField(max_length=40,default=None)
    

class CustomerCheckout(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200,null=True,default = None)
    total_amount = models.FloatField()
    payment_signature = models.CharField(max_length=200,null=True,default = None)
    reciept_num = models.CharField(max_length=200)
    delivery_address =  models.CharField(max_length=2000)
    delivery_phone =  models.CharField(max_length=20)
    date = models.CharField(max_length=10)
    pincode = models.IntegerField(max_length=6, default='000000')
    payment_complete = models.IntegerField(default = 0)
    payedon = models.DateTimeField(auto_now_add=True)

class customerPayedProducts(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    checkout_details = models.ForeignKey(CustomerCheckout, on_delete=models.CASCADE, null=False, blank=False)