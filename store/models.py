from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField()  # when you use ImageField you should install Pillow module
    price = models.FloatField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)  # models.NULL means that if we remove the author of some products then the author attribute of Product object will be null
    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.JSONField(default=dict)
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title