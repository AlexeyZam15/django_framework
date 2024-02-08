from django.core.management.base import BaseCommand

from homework_02.models import Product

import random


class Command(BaseCommand):
    help = 'Add n count to fake products'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество товара для добавления')

    def handle(self, *args, **options):
        count = options['count']
        products = [product for product in Product.objects.all()]
        for product in products:
            product.count += count
            product.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} count to products'))
