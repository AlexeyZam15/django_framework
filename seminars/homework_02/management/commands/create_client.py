from django.core.management.base import BaseCommand

from homework_02.models import Client


class Command(BaseCommand):
    help = 'Create client'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — имя клиента
        — электронная почта клиента
        — номер телефона клиента
        — адрес клиента
        """
        parser.add_argument('name', type=str, help='Client name')
        parser.add_argument('email', type=str, help='Client email')
        parser.add_argument('phone', type=str, help='Client phone')
        parser.add_argument('address', type=str, help='Client address')

    def handle(self, *args, **options):
        name = options['name']
        email = options['email']
        phone = options['phone']
        address = options['address']
        client = Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
        )
        self.stdout.write(f'{client}')
