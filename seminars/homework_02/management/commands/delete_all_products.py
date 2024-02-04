from django.core.management.base import BaseCommand

from homework_02.models import Product


class Command(BaseCommand):
    help = 'Delete all products'

    def handle(self, *args, **options):
        data = Product.objects.all()
        if not data:
            self.stdout.write('No products in database')
            return
        data.delete()
        self.stdout.write('All products deleted')
