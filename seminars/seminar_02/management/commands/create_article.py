from django.core.management.base import BaseCommand

from seminar_02.models import Article


class Command(BaseCommand):
    help = 'Create article'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        ○ заголовок статьи
        ○ содержание статьи
        ○ дата публикации статьи
        ○ автор статьи
        ○ категория статьи
        ○ количество просмотров статьи
        ○ флаг, указывающий, опубликована ли статья
        """
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('category', type=str)
        parser.add_argument('views', type=int)
        parser.add_argument('is_published', type=bool)

    def handle(self, *args, **options):
        article = Article.create_article(
            options['title'],
            options['content'],
            options['date'],
            options['author'],
            options['category'],
            options['views'],
            options['is_published']
        )
        self.stdout.write(f'{article}')
