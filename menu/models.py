from django.db import models
from decimal import Decimal

class Coffee(models.Model):
    TEMPERATURE_CHOICES = [
        ('', 'None'),
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('both', 'Hot & Cold'),
    ]

    GROUP_CHOICES = [
        ('basic', 'Basic Drinks'),
        ('alternative', 'Alternative'),
        ('other', 'Other Drinks'),
        ('addon', 'Add-ons'), 
    ]   

    name = models.CharField(max_length=100)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='basic')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    temperature = models.CharField(max_length=10, choices=TEMPERATURE_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Optional description for coffee information modal")
    order = models.PositiveIntegerField(default=0)

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

    @property
    def price_2_display(self):
        if self.price_2:
            if self.price_2 == self.price_2.to_integral_value():
                return int(self.price_2)
            return self.price_2
        return None

    @property
    def has_two_prices(self):
        return self.price_2 is not None

    def display_volumes(self):
        return ", ".join([v.volume for v in self.volume.all()])


class Toast(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    order = models.PositiveIntegerField(default=0)
    
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
    order = models.PositiveIntegerField(default=0)
    
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
