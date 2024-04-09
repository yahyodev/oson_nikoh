# Generated by Django 4.2.7 on 2024-04-04 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0004_viewedprofile_liked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date of last modification')),
                ('accused', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accused', to='tgbot.user')),
                ('complainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complainer', to='tgbot.user')),
            ],
            options={
                'unique_together': {('complainer', 'accused')},
            },
        ),
    ]