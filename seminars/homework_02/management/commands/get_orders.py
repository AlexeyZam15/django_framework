from django.core.management.base import BaseCommand

from homework_02.models import Order

from homework_02.models import Product


class Command(BaseCommand):
    help = 'Get orders list'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — количество записей
        — фильтр по названию поля и значению
        """
        parser.add_argument('-c', '--count', type=int, help='Count of orders to show', required=False)
        parser.add_argument('-f', '--filter', metavar=('field_name', 'value',), nargs=2, type=str,
                            help='Field name and value to filter', action='append', required=False)
        parser.add_argument('-p', '--products_filter', metavar=('product_field_name', 'value'), nargs=2, type=str,
                            help='Product field name and value to filter', action='append', required=False)

    def handle(self, *args, **options):
        data = Order.objects.order_by('-id').all()
        count = options['count']
        if count is not None:
            data = data[:count]
        filters = options['filter']
        if filters is not None:
            filter_dict = {}
            for field, value in filters:
                filter_dict[field] = value
            data = data.filter(**filter_dict)
        products_filter = options['products_filter']
        if products_filter is not None:
            products_filter_dict = {}
            for field, value in products_filter:
                products_filter_dict[field] = value
            data = data.filter(products__in=Product.objects.filter(**products_filter_dict).all())
        for order in data:
            self.stdout.write(f'{order}')
