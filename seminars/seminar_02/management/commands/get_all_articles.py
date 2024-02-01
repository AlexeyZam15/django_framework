from django.core.management.base import BaseCommand

from seminar_02.models import Article


class Command(BaseCommand):
    help = 'Get all articles list'

    def handle(self, *args, **options):
        articles = Article.get_articles()
        for article in articles:
            self.stdout.write(f'{article.get_info()}')
