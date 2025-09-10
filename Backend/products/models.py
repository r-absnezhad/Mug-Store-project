from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="products/base/")
    is_available = models.BooleanField(default=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
