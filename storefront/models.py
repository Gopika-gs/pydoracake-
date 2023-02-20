import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from adminpannel.models import Products

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
    quantity = models.IntegerField(default=1)
    addedon = models.DateTimeField(auto_now_add=True)
    upgrade = models.CharField(choices=UPGRADE_CHOICES,default='1/2kg', max_length=10)
    content = models.CharField(choices=CONTENT_CHOICES,default='egg', max_length=10)
    message = models.CharField(max_length=40,default=None)

class WishList(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, blank=False)

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

RATING = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

class ProductReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False, blank=False)
    rreview_text = models.TextField()
    review_rating = models.CharField(choices=RATING,max_length=150)