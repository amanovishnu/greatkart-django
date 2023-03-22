from django.db import models
from django.urls import reverse
from category.models import Category
import random

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug  = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, default=random.randint(0,20))

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        return super().get_queryset().filter(variation_category='color', is_active=True) # self approach
        # return super(VariationManager, self).filter(variation_category='color', is_active=True) # instructor approach

    def sizes(self):
        return super().get_queryset().filter(variation_category='size', is_active=True) # self approach
        # return super(VariationManager, self).filter(variation_category='size', is_active=True) # instructor approach


class Variation(models.Model):

    variation_category_choices = [
        ['color', 'color'],
        ['size', 'size'],
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=255, choices=variation_category_choices)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
