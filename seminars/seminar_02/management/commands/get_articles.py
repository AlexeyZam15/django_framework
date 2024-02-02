from django.core.management.base import BaseCommand
from seminar_02.models import Author
from seminar_02.models import Article


class Command(BaseCommand):
    help = 'Get filtered articles list'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', type=int, help='Count of comments', default=None)
        parser.add_argument('-f', '--filter', metavar=('field_name', 'value'),
                            help='Filter comments by field_name and value',
                            type=str, action="append", nargs=2)

    def handle(self, *args, **options):
        count = options['count']
        filters = options['filter']
        data = Article.objects.all()
        if count is not None:
            data = data[:count]
        if filters is not None:
            for filter in filters:
                field_name, value = filter[0], filter[1]
                data = data.filter(**{field_name: value})
        [self.stdout.write(f"{article}") for article in data]
