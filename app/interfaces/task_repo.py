"""
Interface for task repository (DB).
"""

from app.entities.task import ReviewTask

class ITaskRepo:
    def add(self, repo_url: str, pr_number: int, auth_token: str = None) -> int:
        raise NotImplementedError

    def get(self, task_id: int) -> ReviewTask:
        raise NotImplementedError

    def update(self, task_id: int, status: str, results: object = None):
        raise NotImplementedError