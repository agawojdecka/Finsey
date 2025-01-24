from django.core.mail import EmailMessage

from apps.users.models import User


def send_inactivity_notification(user):
    subject = f"Inactivity Notification - user ID: {user.id}"
    body = "You haven't logged into your account for 30 days. If you do not log in for the next 30 days, your account will be deleted."
    from_email = "your-email@gmail.com"
    to_email = [user.email]

    email = EmailMessage(subject, body, from_email, to_email)

    try:
        email.send(fail_silently=False)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_account_deletion_notification(user):
    subject = f"Account Deletion Notification - user ID: {user.id}"
    body = "You haven't logged into your account for 30 days since getting inactivity notification. Your account is being deleted."
    from_email = "your-email@gmail.com"
    to_email = [user.email]

    email = EmailMessage(subject, body, from_email, to_email)

    try:
        email.send(fail_silently=False)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def update_sent_inactivity_notification_status_task():
    users = list(User.objects.filter(sent_inactivity_notification__isnull=False))
    users_to_update = []
    for user in users:
        if user.inactivity_notification_sent_at is not None and user.last_login >= user.inactivity_notification_sent_at:
            user.inactivity_notification_sent_at = None
            users_to_update.append(user)

    User.objects.bulk_update(users_to_update, ['inactivity_notification_sent_at'])
