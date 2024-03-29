from django.contrib.sessions.models import Session
from django.db import models
from django_store import settings
from django.utils.translation import gettext as _
from checkout.models import Transaction

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = (
        models.ImageField()
    )  # when you use ImageField you should install Pillow module
    pdf_file = models.FileField(null=True)
    price = models.FloatField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True
    )  # models.NULL means that if we remove the author of some products then the author attribute of Product object will be null

    @property
    def pdf_file_url(self):
        return (
            settings.SITE_URL + self.pdf_file.url
        )  # notice that we here add settings.py a variable which must be called 'SITE_URL' and give it a value of the main url of the site (the url 'http://127.0.0.1:8000' in this example), then we add our profile as a url to returned value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")


class Order(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


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

    class Meta:
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")


class Cart(models.Model):
    items = models.JSONField(default=dict)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
