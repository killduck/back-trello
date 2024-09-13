# Generated by Django 5.0.4 on 2024-08-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0005_remove_card_activity_activity_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='text',
        ),
        migrations.AddField(
            model_name='activity',
            name='action',
            field=models.TextField(help_text='Введите изменение в карточке', max_length=200, null=True, verbose_name='Изменение в карточке'),
        ),
        migrations.AddField(
            model_name='activity',
            name='comment',
            field=models.TextField(help_text='Введите комментарий к карточке', max_length=500, null=True, verbose_name='Комментарий к карточке'),
        ),
    ]