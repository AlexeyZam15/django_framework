from random import choices
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from lecture_03.models import Author, Post

LOREM = lorem_ipsum.words(100)


class Command(BaseCommand):
    help = "Generate fake authors and posts."

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='users count')

    def handle(self, *args, **kwargs):
        text = LOREM.split()
        count = kwargs.get('count')
        for i in range(1, count + 1):
            author = Author(name=f'Author_{i}', email=f'mail{i}@mail.ru')
            author.save()
            for j in range(1, count + 1):
                post = Post(
                    title=f'Title-{j}', content=" ".join(choices(text, k=64)), author=author)
                post.save()
