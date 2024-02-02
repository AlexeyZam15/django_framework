from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Удаление актёра по id'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        pk = options['id']
        author = Author.delete_author(pk)
        self.stdout.write(f'{author}')
