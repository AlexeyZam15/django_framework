from django.core.management.base import BaseCommand

from homework_02.models import Product


class Command(BaseCommand):
    help = 'Update product'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — id товара
        — название товара
        — описание товара
        — цена товара
        — количество товара
        """
        parser.add_argument('product_name', type=str, help='Product name to update')
        parser.add_argument('-n', '--name', type=str, help='New product name', required=False)
        parser.add_argument('-d', '--description', type=str, help='New product description', required=False)
        parser.add_argument('-p', '--price', type=float, help='New product price', required=False)
        parser.add_argument('-c', '--count', type=int, help='New product count', required=False)

    def handle(self, *args, **options):
        product_name = options['product_name']
        name = options['name']
        description = options['description']
        price = options['price']
        count = options['count']
        product = Product.objects.filter(name=product_name).first()
        if not product:
            self.stdout.write(f'Product {product_name} not found')
            return
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if count is not None:
            product.count = count
        product.save()
        self.stdout.write(f'{product}')
