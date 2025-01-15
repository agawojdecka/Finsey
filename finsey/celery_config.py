from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finsey.settings')

app = Celery('finsey')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test-beat': {
        'task': 'apps.users.tasks.test_celery_beat',
        'schedule': crontab(minute='0', hour='8', day_of_week='1')
    },
    'send_inactivity_notification_task': {
        'task': 'apps.users.tasks.send_inactivity_notification_task',
        'schedule': crontab(minute='0', hour='8', day_of_week='1')
    }
}
