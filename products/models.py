from django.db import models
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)  # Allow null expiry date
    low_stock_threshold = models.IntegerField(default=5)  # Provide a default value

    def __str__(self):
        return self.name

    @property
    def is_expired(self):
        return self.expiry_date and self.expiry_date < date.today()

    def is_low_stock(self):
        return self.quantity < self.low_stock_threshold

    def __str__(self):
        return self.name
    
    