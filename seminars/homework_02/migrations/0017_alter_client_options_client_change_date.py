# Generated by Django 5.0.1 on 2024-02-16 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_02', '0016_orderedproduct_in_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['-reg_date'], 'verbose_name': 'клиент', 'verbose_name_plural': 'клиенты'},
        ),
        migrations.AddField(
            model_name='client',
            name='change_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
