from django.core.management.base import BaseCommand

from seminar_02.models import Author

import random


class Command(BaseCommand):
    help = 'Create fake n authors'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def random_date(self):
        return f'{random.randint(1, 28)}.{random.randint(1, 12)}.{random.randint(1000, 2000)}'

    def handle(self, *args, **options):
        count = options['count']
        """Генерация аргументов для следующих полей:
        ○ имя
        ○ фамилия
        ○ почта
        ○ биография
        ○ день рождения"""
        for i in range(count):
            Author.create_author(
                first_name=f'Name {i}',
                last_name=f'Last name {i}',
                email=f'email{i}@mail.ru',
                bio=f'Bio {i}',
                birth_date=self.random_date()

            )
        self.stdout.write(self.style.SUCCESS(f'Created {count} fake authors'))
