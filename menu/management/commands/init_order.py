from django.core.management.base import BaseCommand
from menu.models import Coffee, Toast, Sweet

class Command(BaseCommand):
    help = 'Initialize order field for existing items'

    def handle(self, *args, **options):
        # Initialize Coffee order
        coffee_groups = ['basic', 'alternative', 'other', 'addon']
        for group in coffee_groups:
            coffees = Coffee.objects.filter(group=group, is_active=True).order_by('id')
            for index, coffee in enumerate(coffees):
                coffee.order = index
                coffee.save()
        
        # Initialize Toast order
        toasts = Toast.objects.filter(is_active=True).order_by('id')
        for index, toast in enumerate(toasts):
            toast.order = index
            toast.save()
        
        # Initialize Sweet order
        sweets = Sweet.objects.filter(is_active=True).order_by('id')
        for index, sweet in enumerate(sweets):
            sweet.order = index
            sweet.save()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized order for all menu items')
        )

