from django.core.management.base import BaseCommand

from homework_02.models import Order


class Command(BaseCommand):
    help = 'Delete all orders'

    def handle(self, *args, **options):
        data = Order.objects.all()
        if not data:
            self.stdout.write('No orders in database')
            return
        data.delete()
        self.stdout.write('All orders deleted')
