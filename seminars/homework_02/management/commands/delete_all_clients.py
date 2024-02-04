from django.core.management.base import BaseCommand

from homework_02.models import Client


class Command(BaseCommand):
    help = 'Delete all clients'

    def handle(self, *args, **options):
        data = Client.objects.all()
        if not data:
            self.stdout.write('No clients in database')
            return
        data.delete()
        self.stdout.write('All clients deleted')
