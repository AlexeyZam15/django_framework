from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Create author'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        ○ имя
        ○ фамилия
        ○ почта
        ○ биография
        ○ день рождения"""
        parser.add_argument('first_name', type=str, help='First name')
        parser.add_argument('last_name', type=str, help='Last name')
        parser.add_argument('email', type=str, help='Email')
        parser.add_argument('bio', type=str, help='Bio')
        parser.add_argument('birth_date', type=str, help='Birth date')

    def handle(self, *args, **options):
        author = Author.create_author(
            first_name=options['first_name'],
            last_name=options['last_name'],
            email=options['email'],
            bio=options['bio'],
            birth_date=options['birth_date']
        )
        self.stdout.write(f'{author}')
