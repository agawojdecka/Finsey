from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.users.models import User
from apps.users.services.inactivity_notifications import (
    send_account_deletion_notification,
    send_inactivity_notification,
    update_sent_inactivity_notification_status_task,
)


@shared_task
def send_inactivity_notification_task() -> None:
    """
    1. Updates inactivity notification status if user logged in
    after sending inactivity notification.
    2. Sends email to all users that haven't been active for 30 days
    about inactivity and potential account deletion.
    3. After next 30 days with no activity, sends deletion notification
    and deletes user.
    """
    update_sent_inactivity_notification_status_task()

    now = timezone.now().date()
    thirty_days_ago = timedelta(days=30)
    delta = now - thirty_days_ago

    inactive_users = list(User.objects.filter(last_login__lte=delta))

    for user in inactive_users:
        if user.inactivity_notification_sent_at is None:
            send_inactivity_notification(user)
            print(f"Inactivity notification sent to user {user.id}")
            user.inactivity_notification_sent_at = now
            user.save()
        elif now - user.inactivity_notification_sent_at >= timedelta(days=30):
            send_account_deletion_notification(user)
            print(f"Account deletion notification sent to user {user.id}")
            user.delete()
