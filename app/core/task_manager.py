"""
Async task orchestration for review tasks.
"""

from logging import Logger
from app.entities.task import ReviewTask, TaskStatus
from app.interfaces.pr_repo import IPullRequestRepo
from app.interfaces.task_repo import ITaskRepo
from app.interfaces.reviewer import IReviewerAgent
from app.interfaces.task_queue import ITaskQueue

class TaskManager(ITaskQueue):
    def __init__(self, logger: Logger, pr_repo: IPullRequestRepo, task_repo: ITaskRepo, reviewer: IReviewerAgent):
        self.logger = logger
        self.pr_repo = pr_repo
        self.task_repo = task_repo
        self.reviewer = reviewer

    def add_review_task(self, task_id: int):
        # This would enqueue the task in Celery (see gateways/task_publisher.py)
        pass

    def consume_task(self, task_id: int):
        self.logger.info(f"Processing task_id: {task_id}")
        self.task_repo.update(task_id, TaskStatus.PROCESSING)
        task = self.task_repo.get(task_id)
        pr = self.pr_repo.get(task.repo_url, task.pr_number, auth_token=task.auth_token)
        review = self.reviewer.review_pr(pr)
        self.task_repo.update(task.id, TaskStatus.COMPLETED, review)