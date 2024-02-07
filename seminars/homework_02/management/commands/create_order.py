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
        order = Order.create_order(client, ordered_products)
        self.stdout.write(f'{order}')
