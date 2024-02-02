from django.core.management.base import BaseCommand

from seminar_02.models import Author


class Command(BaseCommand):
    help = 'Обновление автора'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID автора')
        parser.add_argument('-f', '--first_name', type=str, help='Имя автора', required=False),
        parser.add_argument('-l', '--last_name', type=str, help='Фамилия автора', required=False)
        parser.add_argument('-e', '--email', type=str, help='Email автора', required=False)
        parser.add_argument('-b', '--bio', type=str, help='Биография автора', required=False)
        parser.add_argument('-d', '--birth_date', type=str, help='Дата рождения автора', required=False)

    def handle(self, *args, **options):
        pk = options.get('id')
        for field in Author.fields:
            value = options.get(field)
            if options.get(field) is not None:
                Author.update_author(pk, field, value)
        author = Author.get_author(pk)
        self.stdout.write(f'{author}')
