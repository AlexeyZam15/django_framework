from django.core.management.base import BaseCommand

from homework_02.models import Order


class Command(BaseCommand):
    help = 'Delete order'

    def add_arguments(self, parser):
        """
        Аргументы для следующих полей:
        — id заказа
        """
        parser.add_argument('id', type=int, help='Order id')

    def handle(self, *args, **options):
        pk = options['id']
        order = Order.objects.filter(id=pk).first()
        if not order:
            self.stdout.write(self.style.ERROR(f'Order with id {pk} not found'))
            return
        order.delete()
        self.stdout.write(self.style.SUCCESS(f'Order with id {pk} deleted'))
