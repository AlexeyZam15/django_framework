from django.core.management.base import BaseCommand

from homework_02.models import Client
from homework_02.models import Product
from homework_02.models import OrderedProduct
from homework_02.models import Order


class Command(BaseCommand):
    help = 'Create order'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — имя клиента
        — названия товаров
        """
        parser.add_argument('client_name', type=str, help='Customer-client name')
        parser.add_argument('-p', '--products', metavar=('product_name', 'product_count'), nargs=2, type=str,
                            help='Product name and count for order, separated by space', action='append')

    def handle(self, *args, **options):
        client_name = options['client_name']
        client = Client.objects.filter(name=client_name).first()
        if client is None:
            self.stdout.write(self.style.ERROR(f'Client with name {client_name} not found'))
            return
        ordered_products = options['products']
        products = []
        total_price = 0
        products_count = {}
        for product_name, product_count in ordered_products:
            product = Product.objects.filter(name=product_name).first()
            if product is None:
                self.stdout.write(self.style.ERROR(f'Product {product_name} not found'))
                return
            product_count = int(product_count)
            if product_count <= 0:
                self.stdout.write(self.style.ERROR(f'Count for ordered product must be greater than 0'))
                return
            while product.count < product_count:
                self.stdout.write(self.style.ERROR(f'Not enough products in stock for {product_name}'))
                return
            products.append(product)
            product.count -= product_count
            products_count[product] = product_count
            product.save()
            total_price += product.price * product_count
        if not products:
            self.stdout.write(self.style.ERROR('No products in the order'))
            return
        order = Order.objects.create(
            client=client,
            total_price=total_price,
        )
        for product in products:
            OrderedProduct.objects.create(
                order=order,
                product=product,
                count=products_count[product],
            )
        self.stdout.write(f'{order}')
