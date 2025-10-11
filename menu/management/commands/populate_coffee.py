from django.core.management.base import BaseCommand
from menu.models import Coffee, CoffeeVolume

class Command(BaseCommand):
    help = 'Populate coffee menu with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Coffee.objects.all().delete()
        CoffeeVolume.objects.all().delete()
        
        # Create coffee volumes
        volumes = ['small', 'medium', 'large']
        for volume in volumes:
            CoffeeVolume.objects.create(volume=volume)
        
        # Coffee menu data based on the image
        coffee_data = [
            # Espresso based drinks
            {'name': 'espresso', 'price': 10, 'price_2': None, 'temperature': None},
            {'name': 'doppio', 'price': 12, 'price_2': None, 'temperature': None},
            {'name': 'filter', 'price': 14, 'price_2': 16, 'temperature': 'both'},
            {'name': 'cappuccino', 'price': 14, 'price_2': None, 'temperature': 'both'},
            {'name': 'flat white', 'price': 16, 'price_2': None, 'temperature': 'both'},
            {'name': 'latte', 'price': 18, 'price_2': None, 'temperature': 'both'},
            {'name': 'raf', 'price': 17, 'price_2': 19, 'temperature': 'both'},
            
            # Drip/Pour-over methods
            {'name': 'drip', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'kalita', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'dotyk', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'chemex', 'price': 28, 'price_2': None, 'temperature': None},
            {'name': 'aero press', 'price': 20, 'price_2': None, 'temperature': None},
            {'name': 'syphon', 'price': 27, 'price_2': None, 'temperature': None},
            
            # Cold and special drinks
            {'name': 'cold brew', 'price': 17, 'price_2': None, 'temperature': None},
            {'name': 'espresso tonic', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'espresso orange', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'matcha orange', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'matcha raf', 'price': 17, 'price_2': 19, 'temperature': 'both'},
            {'name': 'matcha tonic', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'matcha latte', 'price': 18, 'price_2': None, 'temperature': 'both'},
            {'name': 'rooibos latte', 'price': 18, 'price_2': None, 'temperature': 'both'},
            {'name': 'karob', 'price': 16, 'price_2': None, 'temperature': 'both'},
            {'name': 'cacao', 'price': 16, 'price_2': None, 'temperature': 'both'},
            {'name': 'masala', 'price': 18, 'price_2': None, 'temperature': None},
            {'name': 'tea', 'price': 16, 'price_2': None, 'temperature': 'both'},
        ]
        
        # Create coffee items
        for item in coffee_data:
            coffee = Coffee.objects.create(
                name=item['name'],
                price=item['price'],
                price_2=item['price_2'],
                temperature=item['temperature']
            )
            # Add all volumes to each coffee
            for volume in CoffeeVolume.objects.all():
                coffee.volume.add(volume)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(coffee_data)} coffee items')
        )
