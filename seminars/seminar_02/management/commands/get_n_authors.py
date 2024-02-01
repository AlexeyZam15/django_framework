from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Получает n последних авторов'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество авторов')

    def handle(self, *args, **options):
        count = options['count']
        authors = Author.objects.order_by('-id')[:count]
        for author in authors:
            self.stdout.write(f'{author}')
