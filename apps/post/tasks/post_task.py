from celery import shared_task
import time


@shared_task
def upload_video(x, y):
    time.sleep(30)
    return x, y
