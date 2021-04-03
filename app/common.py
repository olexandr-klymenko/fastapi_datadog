from os import getenv

from redisrpc import RedisRPC
from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://redis:6379/0",
    broker="amqp://user:bitnami@rabbitmq:5672//"
)
celery_app.conf.task_routes = {
    "app.worker.test_celery": "test-queue",
    "app.worker.slow_sql_query": "slow_sql_query-queue",
    "app.worker.exception": "exception-queue",
}

celery_app.conf.update(task_track_started=True)


def get_redis_rpc() -> RedisRPC:
    return RedisRPC(getenv("REDISRPC_CHANNEL"))
