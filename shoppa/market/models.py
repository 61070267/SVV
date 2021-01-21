from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShopOwner(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(max_length=50)
    shop_address = models.TextField()
    shop_desc = models.CharField(max_length=400)
    shop_icon = models.ImageField(upload_to='icon')
    shop_bg = models.ImageField(upload_to='bg')

class Customer(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cus_fname = models.CharField(max_length=30)
    cus_lname = models.CharField(max_length=30)
    cus_address = models.TextField()
    cus_img = models.ImageField(upload_to='img')

class Cart(models.Model):
    customer_username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    sum_cost = models.FloatField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=30)

class SubCategory(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=None)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    prod_desc = models.TextField()
    img = models.ImageField(upload_to='product', default='noimg.jpg')
    shop = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, default=None, null=True)

class Payment(models.Model):
    cart_id = models.OneToOneField(Cart, related_name='payment', on_delete=models.CASCADE)
    amount = models.FloatField()

    payment_type = (
        ('01', 'iBank Pay'),
        ('02', 'Youeself')
    )
    payment = models.CharField(max_length=2, choices=payment_type, default='01')
    
class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0)
    item_price = models.FloatField(default=0)
