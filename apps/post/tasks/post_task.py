from celery import shared_task
import time


@shared_task(name="upload-video")
def upload_video(x, y):
    time.sleep(30)
    return x + y
