from datetime import datetime

from django.db import models
from django.conf import settings

from .utils import generate_unique_slug


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=510, null=True, blank=True)
    thumbnail = models.URLField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ending_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        updating = self.pk is not None
        
        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
            super().save(*args, **kwargs)
        else:
            self.slug = generate_unique_slug(self, self.title)
            super().save(*args, **kwargs)

    @property
    def active(self):
        return True


class PlacedBid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.title
