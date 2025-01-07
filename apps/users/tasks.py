from celery import shared_task


@shared_task
def test_celery_beat():
    """
    Simple task to test Celery beat
    """
    print("Task completed")
