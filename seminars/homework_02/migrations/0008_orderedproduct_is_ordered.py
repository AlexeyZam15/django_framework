# Generated by Django 5.0.1 on 2024-02-15 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_02', '0007_rename_or_order_orderedproduct_in_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproduct',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]