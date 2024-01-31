import random

from django.core.management.base import BaseCommand

from seminar_02.models import Coin


class Command(BaseCommand):
    help = 'Create coin'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        print(f'Creating {count} coins:')
        for _ in range(count):
            coin = Coin(side=random.choice(Coin.choices))
            coin.save()
            print(coin)
