from django.core.management.base import BaseCommand

from homework_02.models import Product


class Command(BaseCommand):
    help = 'Delete product'

    def add_arguments(self, parser):
        """
        Аргументы для следующих полей:
        — id товара
        """
        parser.add_argument('product_name', type=str, help='Product name to delete')

    def handle(self, *args, **options):
        product_name = options['product_name']
        product = Product.objects.filter(name=product_name).first()
        if not product:
            self.stdout.write(f'Product {product_name} not found')
            return
        product.delete()
        self.stdout.write(f'{product}')
