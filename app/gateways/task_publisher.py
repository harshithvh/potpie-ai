"""
Celery task publisher for review tasks.
"""

from app.interfaces.task_queue import ITaskQueue

class CeleryTaskPublisher(ITaskQueue):
    def __init__(self, celery_task):
        self.celery_task = celery_task

    def add_review_task(self, task_id: int):
        self.celery_task.delay(task_id)

    def consume_task(self, task_id: int):
        # Not used here; worker consumes tasks
        pass