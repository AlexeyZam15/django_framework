# Generated by Django 5.0.1 on 2024-02-17 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminar_02', '0009_alter_comment_article_alter_comment_author'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together=set(),
        ),
    ]