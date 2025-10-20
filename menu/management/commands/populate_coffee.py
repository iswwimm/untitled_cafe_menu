from django.core.management.base import BaseCommand
from menu.models import Coffee

class Command(BaseCommand):
    help = 'Populate coffee menu with sample data and assign groups'

    def handle(self, *args, **options):
        # Clear existing data
        Coffee.objects.all().delete()
        
        
        coffee_data = [
            # Basic Drinks
            {'name': 'espresso', 'price': 10, 'price_2': None, 'temperature': None, 'group': 'basic'},
            {'name': 'doppio', 'price': 12, 'price_2': None, 'temperature': None, 'group': 'basic'},
            {'name': 'filter', 'price': 14, 'price_2': 16, 'temperature': 'both', 'group': 'basic'},
            {'name': 'cappuccino', 'price': 14, 'price_2': None, 'temperature': 'both', 'group': 'basic'},
            {'name': 'flat white', 'price': 16, 'price_2': None, 'temperature': 'both', 'group': 'basic'},
            {'name': 'latte', 'price': 18, 'price_2': None, 'temperature': 'both', 'group': 'basic'},
            {'name': 'raf', 'price': 17, 'price_2': 19, 'temperature': 'both', 'group': 'basic'},

            # Alternative
            {'name': 'drip', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'alternative'},
            {'name': 'kalita', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'alternative'},
            {'name': 'dotyk', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'alternative'},
            {'name': 'chemex', 'price': 28, 'price_2': None, 'temperature': None, 'group': 'alternative'},
            {'name': 'aero press', 'price': 20, 'price_2': None, 'temperature': None, 'group': 'alternative'},
            {'name': 'syphon', 'price': 27, 'price_2': None, 'temperature': None, 'group': 'alternative'},

            # Other Drinks
            {'name': 'cold brew', 'price': 17, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'espresso tonic', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'espresso orange', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'matcha orange', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'matcha raf', 'price': 17, 'price_2': 19, 'temperature': 'both', 'group': 'other'},
            {'name': 'matcha tonic', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'matcha latte', 'price': 18, 'price_2': None, 'temperature': 'both', 'group': 'other'},
            {'name': 'rooibos latte', 'price': 18, 'price_2': None, 'temperature': 'both', 'group': 'other'},
            {'name': 'karob', 'price': 16, 'price_2': None, 'temperature': 'both', 'group': 'other'},
            {'name': 'cacao', 'price': 16, 'price_2': None, 'temperature': 'both', 'group': 'other'},
            {'name': 'masala', 'price': 18, 'price_2': None, 'temperature': None, 'group': 'other'},
            {'name': 'tea', 'price': 16, 'price_2': None, 'temperature': 'both', 'group': 'other'},

            # Add-ons
            {'name': 'Vanilla Syrup', 'price': 5, 'price_2': None, 'temperature': None, 'group': 'addon'},
        ]

        
        # Create coffee items
        for item in coffee_data:
            Coffee.objects.create(
                name=item['name'],
                price=item['price'],
                price_2=item['price_2'],
                temperature=item['temperature'],
                is_active=True,
                group=item['group']  # якщо потрібно, додай поле group у модель Coffee
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(coffee_data)} coffee items')
        )
