"""
Interface for task queue (Celery, etc).
"""

class ITaskQueue:
    def add_review_task(self, task_id: int):
        raise NotImplementedError

    def consume_task(self, task_id: int):
        raise NotImplementedError