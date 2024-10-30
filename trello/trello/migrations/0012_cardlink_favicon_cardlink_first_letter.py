# Generated by Django 5.0.4 on 2024-09-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0011_cardlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlink',
            name='favicon',
            field=models.CharField(blank=True, help_text='Введите ссылку для фавикона', max_length=50, null=True, verbose_name='Имя ссылки для фавикона'),
        ),
        migrations.AddField(
            model_name='cardlink',
            name='first_letter',
            field=models.CharField(blank=True, help_text='Введите первую букву ссылки', max_length=10, null=True, verbose_name='первая буква ссылки'),
        ),
    ]
