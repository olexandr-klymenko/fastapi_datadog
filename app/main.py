import logging
import os

from datadog import initialize, statsd
from fastapi import FastAPI, BackgroundTasks

from app.common import celery_app

initialize(statsd_host=os.environ.get('DATADOG_HOST'))

logger = logging.getLogger(__name__)

app = FastAPI()


def celery_on_message(body):
    logger.warning(body)


def background_on_message(task):
    logger.warning(task.get(on_message=celery_on_message, propagate=False))


@app.get("/{word}")
async def root(word: str, background_task: BackgroundTasks):
    statsd.increment('docker_compose_example.page.views')
    task_name = "app.worker.test_celery"

    task = celery_app.send_task(task_name, args=[word])
    print(task)
    background_task.add_task(background_on_message, task)

    return {"message": "Word received"}
