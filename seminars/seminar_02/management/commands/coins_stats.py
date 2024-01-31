from django.core.management.base import BaseCommand

from seminar_02.models import Coin


class Command(BaseCommand):
    help = 'Собирает статистику о монетах'

    def add_arguments(self, parser):
        """Необязательный аргумент количества выводимых записей"""
        parser.add_argument('count', type=int, default=None)

    def handle(self, *args, **options):
        count = options['count']
        stats = Coin.get_statistics(count)
        self.stdout.write(f'{stats}')
