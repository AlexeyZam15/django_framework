from django.core.management.base import BaseCommand

from seminar_02.models import Coin


class Command(BaseCommand):
    help = 'Получает n последних монет'

    def add_arguments(self, parser):
        """Необязательный аргумент количества выводимых записей"""
        parser.add_argument('count', type=int, default=None)

    def handle(self, *args, **options):
        count = options['count']
        coins = Coin.get_coins(count)
        for coin in coins:
            self.stdout.write(f'{coin}')
