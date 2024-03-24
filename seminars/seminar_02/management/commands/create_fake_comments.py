from django.core.management.base import BaseCommand

from seminar_02.models import Author
from seminar_02.models import Article
from seminar_02.models import Comment

import random


class Command(BaseCommand):
    help = 'Create fake n articles'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        """Генерация аргументов для следующих полей:
        ○ автор
        ○ статья
        ○ комментарий
        """
        authors = [author for author in Author.objects.all()]
        articles = [article for article in Article.objects.filter(is_published=True).all()]
        data = [Comment(
            author=random.choice(authors),
            article=random.choice(articles),
            comment=f'Comment_{i}')
            for i in range(count)]
        Comment.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS(f'{count} fake comments created!'))
