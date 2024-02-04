from django.core.management.base import BaseCommand

from homework_02.models import Client


class Command(BaseCommand):
    help = 'Update client'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — id клиента
        — имя клиента
        — электронная почта клиента
        — номер телефона клиента
        — адрес клиента
        """
        parser.add_argument('client', type=str, help='Client name')
        parser.add_argument('-n', '--name', type=str, help='Client name', required=False)
        parser.add_argument('-e', '--email', type=str, help='Client email', required=False)
        parser.add_argument('-p', '--phone', type=str, help='Client phone', required=False)
        parser.add_argument('-a', '--address', type=str, help='Client address', required=False)

    def handle(self, *args, **options):
        client_name = options['client']
        name = options['name']
        email = options['email']
        phone = options['phone']
        address = options['address']
        client = Client.objects.filter(name=client_name).first()
        if not client:
            self.stdout.write(self.style.ERROR(f'Client {client_name} not found'))
            return
        if name is not None:
            client.name = name
        if email is not None:
            client.email = email
        if phone is not None:
            client.phone = phone
        if address is not None:
            client.address = address
        client.save()
        self.stdout.write(f'{client}')
