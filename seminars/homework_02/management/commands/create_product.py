from django.core.management.base import BaseCommand

from homework_02.models import Product


class Command(BaseCommand):
    help = 'Create product'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — название товара
        — описание товара
        — цена товара
        — количество товара
        """
        parser.add_argument('name', type=str, help='Product name')
        parser.add_argument('description', type=str, help='Product description')
        parser.add_argument('price', type=float, help='Product price')
        parser.add_argument('count', type=int, help='Product count')

    def handle(self, *args, **options):
        name = options['name']
        description = options['description']
        price = options['price']
        count = options['count']
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            count=count,
        )
        self.stdout.write(f'{product}')