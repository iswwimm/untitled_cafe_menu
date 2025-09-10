from django.db import models

# ---------------- CoffeeVolume ----------------
class CoffeeVolume(models.Model):
    volume = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.volume 

# ---------------- Coffee ----------------
class Coffee(models.Model):
    TEMPERATURE_CHOICES = [
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('both', 'Hot & Cold'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    volume = models.ManyToManyField(CoffeeVolume, blank=True)
    temperature = models.CharField(max_length=10, choices=TEMPERATURE_CHOICES, default='hot')

    def __str__(self):
        return self.name

    def display_volumes(self):
        return ", ".join([v.volume for v in self.volume.all()])

# ---------------- Toast ----------------
class Toast(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# ---------------- Sweet ----------------
class Sweet(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/images/', blank=True, null=True)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name
