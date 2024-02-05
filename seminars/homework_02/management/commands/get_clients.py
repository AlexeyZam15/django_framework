from django.core.management.base import BaseCommand

from homework_02.models import Client


class Command(BaseCommand):
    help = 'Get clients list'

    def add_arguments(self, parser):
        """Аргументы для следующих полей:
        — количество записей
        — фильтр по названию поля и значению
        """
        parser.add_argument('-c', '--count', type=int, help='Count of clients to show', required=False)
        parser.add_argument('-f', '--filter', metavar=('field_name', 'value',), nargs=2, type=str,
                            help='Field name and value to filter', action='append', required=False)

    def handle(self, *args, **options):
        data = Client.objects.order_by('-id').all()
        count = options['count']
        if count is not None:
            data = data[:count]
        filters = options['filter']
        if filters is not None:
            filter_dict = {}
            for field, value in filters:
                filter_dict[field] = value
            data = data.filter(**filter_dict)
        for client in data:
            self.stdout.write(f'{client}')
