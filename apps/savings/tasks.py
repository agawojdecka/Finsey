from celery import shared_task

from apps.savings.services.notifications import send_goal_achievement_notification


@shared_task
def send_goal_achievement_notification_task():
    """
    Sends email with congratulations to all users that have achieved a goal.
    """
    send_goal_achievement_notification()
