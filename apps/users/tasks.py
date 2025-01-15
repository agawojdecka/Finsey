from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.users.models import User
from apps.users.services.inactivity_notifications import send_inactivity_notification


@shared_task
def test_celery_beat():
    """
    Simple task to test Celery beat
    """
    print("Task completed")


@shared_task
def send_inactivity_notification_task():
    """
    Sends email to all users that haven't been active since 30 days
    """
    inactive_users = list(User.objects.filter(last_login__lte=timezone.now() - timedelta(days=30)))

    for user in inactive_users:
        send_inactivity_notification(user)
        print(f"Inactivity notification sent to user {user.id}")
