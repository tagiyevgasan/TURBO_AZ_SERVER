# Generated by Django 2.2.18 on 2023-06-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230612_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_chat_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]