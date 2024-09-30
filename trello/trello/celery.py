import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'trello.settings')

app = Celery('trello')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

# заносим таски в очередь
app.conf.beat_schedule = {
    'every': {
        'task': 'trello.tasks.checking_expired_cards',
        # по умолчанию выполняет каждые 30 мин., гибко настраивается
        # 'schedule': crontab(hour='*/1'),
        'schedule': crontab(minute='*/30'),
    },
}
