# Generated by Django 4.2.7 on 2024-05-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0010_remove_user_notification_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='premium',
            field=models.BooleanField(default=False, verbose_name='premium'),
        ),
    ]