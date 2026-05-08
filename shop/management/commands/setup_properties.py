from django.core.management.base import BaseCommand
from shop.models.products import ProductProperty

class Command(BaseCommand):
    help = 'Pre-populate default properties globally'

    def handle(self, *args, **kwargs):
        properties = [
            'Color', 'Size', 'Material', 'Screen Size', 'RAM', 
            'Storage', 'Dimensions', 'Weight', 'Power/Wattage', 'Warranty'
        ]
        for prop in properties:
            ProductProperty.objects.get_or_create(name=prop)
        self.stdout.write(self.style.SUCCESS('Successfully populated default properties.'))
