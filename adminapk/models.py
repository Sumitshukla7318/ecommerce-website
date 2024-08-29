from django.db import models

class Admin_register(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=50)
    des = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    des = models.CharField(max_length=100)
    image = models.FileField(upload_to='uploads/products/')

class Block(models.Model):
    adminn = models.ForeignKey(Admin_register, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now_add=True)

class AdminOTP(models.Model):
    admin = models.ForeignKey(Admin_register, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin.email
