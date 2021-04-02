import logging
import os

from datadog import initialize, statsd
from fastapi import FastAPI, BackgroundTasks

from app.common import celery_app
from app.crud.routers.dealers import router as dealers_router
from app.crud.routers.info import router as info_router
from app.crud.routers.vehicles import router as vehicles_router

initialize(statsd_host=os.environ.get('DATADOG_HOST'))

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(dealers_router, prefix="/dealers", tags=["dealers"])
app.include_router(vehicles_router, prefix="/vehicles", tags=["vehicles"])
app.include_router(info_router)


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
