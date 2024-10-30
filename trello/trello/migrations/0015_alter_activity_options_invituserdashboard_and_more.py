# Generated by Django 5.0.4 on 2024-10-30 23:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0014_serviceimages_alter_activity_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['-id'], 'verbose_name': 'Действия', 'verbose_name_plural': 'Действие'},
        ),
        migrations.CreateModel(
            name='InvitUserDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.TextField(help_text='Введите значение хэша', verbose_name='Значение хэша')),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_user_invait', to='trello.dashboard', verbose_name='Дашборд')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dashboard_invate', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddConstraint(
            model_name='invituserdashboard',
            constraint=models.UniqueConstraint(fields=('dashboard', 'user'), name='unique_dashboard_user_hash'),
        ),
    ]
