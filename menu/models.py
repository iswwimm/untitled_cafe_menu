from django.db import models
from decimal import Decimal

class CoffeeVolume(models.Model):
    volume = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.volume


class Coffee(models.Model):
    TEMPERATURE_CHOICES = [
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('both', 'Hot & Cold'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    volume = models.ManyToManyField(CoffeeVolume, blank=True, related_name='coffees')
    temperature = models.CharField(max_length=10, choices=TEMPERATURE_CHOICES, default='hot')
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        # повертаємо ціле число, якщо воно ціле, інакше Decimal (наприклад 45.5)
        if self.price == self.price.to_integral_value():
            return int(self.price)
        return self.price

    def display_volumes(self):
        return ", ".join([v.volume for v in self.volume.all()])


class Toast(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        if self.price == self.price.to_integral_value():
            return int(self.price)
        return self.price


class Sweet(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        if self.price == self.price.to_integral_value():
            return int(self.price)
        return self.price
