# Generated by Django 5.0.4 on 2024-09-11 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0009_card_execute_cardfile_cardimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, help_text='Введите расширение фото', max_length=50, null=True, verbose_name='Расширение фото')),
            ],
        ),
        migrations.AddField(
            model_name='cardfile',
            name='image',
            field=models.BooleanField(default=False, verbose_name='фото или нет'),
        ),
        migrations.AddField(
            model_name='cardimg',
            name='image',
            field=models.BooleanField(default=True, verbose_name='фото или нет'),
        ),
    ]