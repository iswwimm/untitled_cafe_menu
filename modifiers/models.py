from django.db import models

class Item(models.Model):

    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
