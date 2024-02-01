from django.core.management.base import BaseCommand

from seminar_02.models import Article
from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Update article'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='Article id')
        parser.add_argument('-t', '--title', type=str, help='Title', required=False)
        parser.add_argument('-c', '-content', type=str, help='Content', required=False)
        parser.add_argument('-a', '--author', type=int, help='Author id', required=False)
        parser.add_argument('-cat', '--category', type=str, help='Category', required=False)
        parser.add_argument('-vi', '--views', type=int, help='Views', required=False)
        parser.add_argument('-p', '--is_published', type=str, help='Is published', required=False)

    def handle(self, *args, **options):
        pk = options['id']
        author_id = options.get('author')
        if author_id is not None:
            author = Author.get_author(author_id)
            if author is not None:
                Article.update_article(pk, 'author', author)

        published = options.get('is_published')
        if published is not None and published in ('True', 'False'):
            Article.update_article(pk, 'is_published', eval(published))

        for field in Article.fields:
            value = options.get(field)
            if value is not None:
                Article.update_article(pk, field, value)
        article = Article.get_article(pk)
        self.stdout.write(f'{article}')
