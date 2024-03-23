from django.core.management.base import BaseCommand

from homework_02.models import Product

import random


class Command(BaseCommand):
    help = 'Create n fake products'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake products to create')

    def handle(self, *args, **options):
        """
        Генерация аргументов для следующих полей:
        — название товара
        — описание товара
        — цена товара
        — количество товара
        """
        count = options['count']
        products = Product.objects.all()
        if products:
            last_id = products.order_by('-id')[0].id
        else:
            test = Product.objects.create(
                name='test',
                description='test',
                price=1,
                count=1)
            last_id = test.id
            test.delete()
        data = []
        for i in range(count):
            pk = last_id + i
            data.append(Product(
                name=f'Product_{pk}',
                description=f'Description_{pk}',
                price=random.randint(10, 1000),
                count=random.randint(5, 70)
            ))
        Product.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS(f'Created {count} fake products'))
        return
