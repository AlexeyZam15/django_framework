from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Get authors'

    def handle(self, *args, **options):
        authors = Author.get_authors()
        for author in authors:
            self.stdout.write(f'{author}')
