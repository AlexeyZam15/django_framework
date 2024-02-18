from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Delete all authors'

    def handle(self, *args, **options):
        authors = Author.objects.all()
        if not authors:
            self.stdout.write(self.style.WARNING('No authors found'))
            return
        authors.delete()
        self.stdout.write(self.style.SUCCESS('All authors deleted'))
        return
