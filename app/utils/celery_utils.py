"""
Celery task closure helper.
"""

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_conn_string = os.getenv("REDIS_CONN_STRING", "redis://localhost:6379")

celery_app = Celery(
    "tasks",
    broker=redis_conn_string + "/0",
    backend=redis_conn_string + "/1"
)

task_manager = None  # This will be injected at runtime


@celery_app.task(name="run_review_task")
def run_review_task(task_id: int):
    if task_manager is None:
        raise RuntimeError("Task manager is not initialized")
    task_manager.consume_task(task_id)
