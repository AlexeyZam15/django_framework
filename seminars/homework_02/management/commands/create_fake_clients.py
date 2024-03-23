from django.core.management.base import BaseCommand

from homework_02.models import Client

import random


class Command(BaseCommand):
    help = 'Create fake n clients'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake clients to create')

    def handle(self, *args, **options):
        """
        Генерация аргументов для следующих полей:
        — имя клиента
        — электронная почта клиента
        — номер телефона клиента
        — адрес клиента
        """
        count = options['count']
        clients = Client.objects.all()
        if clients:
            last_id = clients.order_by('-id')[0].id
        else:
            test_client = Client.objects.create(
                name='test',
                email=f'test@mail.ru',
                phone=f'test',
                address=f'test')

            last_id = test_client.id
            test_client.delete()
        data = []
        for i in range(count):
            pk = last_id + i
            data.append(Client(
                name=f'Client_{pk}',
                email=f'client_{pk}@mail.ru',
                phone=f'+7{random.randint(100000000, 999999999)}',
                address=f'Address_{pk}'
            ))
        Client.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS(f'Created {count} fake clients'))
