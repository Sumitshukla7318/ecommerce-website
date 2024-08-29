from django.db import models
from adminapk.models import Product
from django.utils import timezone
from datetime import timedelta


class Customer(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    father=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    pass1=models.CharField(max_length=20)
    Phone=models.CharField(max_length=10)
    image=models.FileField(upload_to="uploads/users/",null=True)


class Cart(models.Model):
        customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        quantity=models.IntegerField(default=1)
    
class customer_otp(models.Model):
      customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
      otp=models.CharField(max_length=6)
      created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.state}, {self.country}'
    


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default='Pending')
    otp = models.CharField(max_length=6, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)


    def is_returnable(self):
        if self.confirmed_at:
            return timezone.now() <= self.confirmed_at + timedelta(days=10)
        return False

    def __str__(self):
        return f'Order {self.id} by {self.customer.fname}'
      






