from django.core.management.base import BaseCommand
from seminar_02.models import Comment


class Command(BaseCommand):
    help = 'Delete all comments'

    def handle(self, *args, **options):
        comments = Comment.objects.all()
        if not comments:
            self.stdout.write(self.style.SUCCESS('No comments found'))
            return
        comments.delete()
        self.stdout.write(self.style.SUCCESS('Comments deleted'))
        return
