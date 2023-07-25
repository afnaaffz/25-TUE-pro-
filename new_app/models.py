from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.



class Login(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_customer=models.BooleanField(default=False)


class Register(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Login, on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.IntegerField()
    phone_no = models.CharField(max_length=10, unique = True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.address)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Variant(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    variant_name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.variant_name


class VariantValue(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(default=0)
    primary_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='primary_products')
    secondary_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='secondary_products')
    image = models.FileField(upload_to='image/')

    def __str__(self):
        return self.product_name


class VariantAdd(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    primary_variant =  models.ForeignKey(Variant, on_delete=models.CASCADE)
    product_stock = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.id





class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Login, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.customer}"


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.cart} - {self.product}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('ordered', 'Ordered'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address= models.CharField(max_length=255)
    phone = models.CharField(max_length=50, default='', blank=True)
    district = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True, blank=True,related_name='created_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order by {self.customer} - {self.created_date}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order} - {self.product}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='banners/')
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_url = models.CharField(max_length=100, default="/shop")
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name
