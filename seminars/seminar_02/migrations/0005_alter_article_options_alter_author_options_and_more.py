# Generated by Django 5.0.1 on 2024-02-17 06:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar_02', '0004_alter_author_birth_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-change_date'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['-change_date'], 'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='coin',
            options={'ordering': ['-time'], 'verbose_name': 'Монета', 'verbose_name_plural': 'Монеты'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_modified'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='article',
            name='change_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='author',
            name='change_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='author',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('author', 'article')},
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together={('author', 'article')},
        ),
    ]