from django.core.mail import EmailMessage

from apps.savings.models import Goal


def send_goal_achievement_notification() -> None:
    """Send email notifications to users who have completed their goal."""
    goals = Goal.objects.select_related('user').filter(
        is_completed=True,
        notification_sent=False,
    )

    for goal in goals:
        user = goal.user
        subject = f"Goal Achievement - user ID: {user.id}"
        body = f"Congratulations! You have achieved your goal: {goal.title}"
        from_email = "your-email@gmail.com"
        to_email = [user.email]

        email = EmailMessage(subject, body, from_email, to_email)

        try:
            email.send(fail_silently=False)
            print("Goal achievement notification sent successfully.")
            goal.notification_sent = True
            goal.save()
        except Exception as e:
            print(f"Failed to send email: {e}")
