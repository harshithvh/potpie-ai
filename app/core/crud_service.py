"""
CRUD logic for review tasks and results.
"""

from logging import Logger
from typing import Optional, Tuple
from app.entities.task import ReviewTask, TaskStatus
from app.interfaces.task_repo import ITaskRepo
from app.interfaces.task_queue import ITaskQueue

class CrudService:
    def __init__(self, logger: Logger, task_repo: ITaskRepo, task_queue: ITaskQueue):
        self.logger = logger
        self.task_repo = task_repo
        self.task_queue = task_queue

    def create_review_task(self, repo_url: str, pr_number: int, auth_token: str = None) -> int:
        task_id = self.task_repo.add(repo_url, pr_number, auth_token)
        self.task_queue.add_review_task(task_id)
        return task_id

    def get_task_status(self, task_id: int) -> TaskStatus:
        task = self.task_repo.get(task_id)
        return task.status

    def get_task_result(self, task_id: int) -> Tuple[TaskStatus, Optional[object]]:
        task = self.task_repo.get(task_id)
        if task.status == TaskStatus.COMPLETED:
            return task.status, task.results
        return task.status, None