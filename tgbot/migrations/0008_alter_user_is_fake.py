# Generated by Django 4.2.7 on 2024-04-09 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0007_necessarylink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_fake',
            field=models.BooleanField(default=False, verbose_name='is fake'),
        ),
    ]
