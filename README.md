# START PROJECT

## ACTIVATE VIRTUAL ENVIRONMENT

Make sure virtual environment is setup, and active.

## INSTALL PACKAGES

Make sure requirements.txt is there, now install all the packages with below command

```
pip install -r requirements.txt
```

## START SERVER

```
python manage.py runserver
```

# START TASK QUEUE

## START CONSUMER (CELERY WORKER/PROCESS)

Start consumer , celery worker or process to process the tasks.

```shell
celery -A core worker -l INF
```

## START TASK MONITORING TOOL (FLOWER)

```shell
celery -A core flower
```

