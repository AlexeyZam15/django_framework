from django.core.management.base import BaseCommand

from homework_02.models import Client
from homework_02.models import Product
from homework_02.models import OrderedProduct
from homework_02.models import Order

import random


class Command(BaseCommand):
    help = 'Create fake n orders'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake orders to create')

    def handle(self, *args, **options):

        clients = [client for client in Client.objects.all()]
        products = [product for product in Product.objects.all()]
        orders_count = options['count']
        created_count = 0
        for _ in range(orders_count):
            """
            Генерация аргументов для следующих полей:
            — имя клиента
            — название товара
            — количество заказанного товара
            """
            client = random.choice(clients)
            ordered_products = []
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                count = random.randint(1, 10)
                try:
                    ordered_product = OrderedProduct.create_ordered_product(product.name, count, )
                    ordered_products.append(ordered_product)
                    ordered_product.save()
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(str(e)))
                    continue
            try:
                Order.create_order(client, ordered_products)
            except ValueError as e:
                self.stdout.write(self.style.ERROR(str(e)))
                continue
            created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} fake orders'))
