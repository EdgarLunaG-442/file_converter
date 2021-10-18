import os
from time import sleep
from helpers import changeTaskState,convertFile

from celery import Celery


os.environ.setdefault("REDIS_HOST", "localhost")
UPLOAD_DIRECTORY = "../data/input"
OUTPUT_DIRECTORY = "../data/output"

celery_app = Celery(
    "tareas",
    broker=f'redis://{os.environ["REDIS_HOST"]}:6379/0',
    backend=f'redis://{os.environ["REDIS_HOST"]}:6379/0',
)



@celery_app.task(name="procesar_tarea")
def cron(id_task):
    convertFile(id_task)
    changeTaskState(id_task)
