from django.core.management.base import BaseCommand

from seminar_02.models import Author
from seminar_02.models import Article

import random


class Command(BaseCommand):
    help = 'Create fake n articles'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        """Генерация аргументов для следующих полей:
        ○ заголовок статьи
        ○ содержание статьи
        ○ дата публикации статьи
        ○ автор статьи
        ○ категория статьи
        ○ количество просмотров статьи
        ○ флаг, указывающий, опубликована ли статья
        """
        authors = [author for author in Author.objects.all()]
        for i in range(count):
            data = {
                'title': f'Title{i}',
                'content': f'Content{i}',
                'author': random.choice(authors),
                'category': f'Category{i}',
                'views': random.randint(0, 100),
                'is_published': random.choice([True, False])}
            Article.create_article(data)
        self.stdout.write(self.style.SUCCESS(f'Created {count} fake articles'))
