import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery(
    "config",
    broker=settings.CELERY_BROKER_URL,
    backend="rpc://",
)

celery_app.config_from_object(settings)
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "reset-today-cups": {
        "task": "apps.account.tasks.reset_today_cups",
        "schedule": crontab(minute="0", hour="0"),
    },
}
