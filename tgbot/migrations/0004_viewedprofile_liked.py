# Generated by Django 4.2.7 on 2024-04-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0003_user_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedprofile',
            name='liked',
            field=models.BooleanField(default=False, verbose_name='liked'),
        ),
    ]
