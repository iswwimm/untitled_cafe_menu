# menu/models.py
from django.db import models

class Coffee(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    milk_alternatives = models.CharField(max_length=200, blank=True)
    preparation_method = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to='menu/images/')

    def __str__(self):
        return self.name

class Toast(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    preparation_method = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to='menu/images/')

    def __str__(self):
        return self.name

class Sweet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    preparation_method = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to='menu/images/')

    def __str__(self):
        return self.name
