from django.core.management.base import BaseCommand

from seminar_02.models import Comment

from random import randint


class Command(BaseCommand):
    help = 'Change random fake comments'

    def handle(self, *args, **options):
        comments = Comment.objects.all()
        for comment in comments:
            if randint(0, 1) == 1:
                comment.comment += ' changed'
                comment.save()
        self.stdout.write(self.style.SUCCESS('Fake comments changed'))
        return
