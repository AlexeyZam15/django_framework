from django.core.management.base import BaseCommand

from seminar_02.models import Article


class Command(BaseCommand):
    help = 'Удаление статьи по id'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        pk = options['id']
        article = Article.delete_article(pk)
        self.stdout.write(f'{article}')
