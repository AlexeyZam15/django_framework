from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Получает актёра по id'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        author = Author.get_author(options['id'])
        self.stdout.write(f'{author}')
