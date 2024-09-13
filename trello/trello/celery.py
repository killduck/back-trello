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
        'task': 'trello.tasks.repeat_order_make',
        # 'schedule': crontab(hour='*/3'),  # по умолчанию выполняет каждую минуту, очень гибко настраивается
        'schedule': crontab(minute='*/1'),
    },
}
