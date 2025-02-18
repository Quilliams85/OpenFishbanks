import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishbanks.settings')

app = Celery('fishbanksapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule the task to run every minute
app.conf.beat_schedule = {
    'update-population-every-minute': {
        'task': 'fishbanksapp.tasks.update_population',
        'schedule': crontab(minute='*/1'),  # Runs every minute
    },
}