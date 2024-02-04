from django.core.management.base import BaseCommand

from homework_02.models import Client


class Command(BaseCommand):
    help = 'Delete client'

    def add_arguments(self, parser):
        """
        Аргументы для следующих полей:
        — имя клиента
        """
        parser.add_argument('name', type=str, help='Client name')

    def handle(self, *args, **options):
        client_name = options['name']
        client = Client.objects.filter(name=client_name).first()
        if not client:
            self.stdout.write(self.style.ERROR(f'Client {client_name} not found'))
            return
        client.delete()
        self.stdout.write(f'{client}')
