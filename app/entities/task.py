"""
Task and status models.
"""

from enum import Enum
from typing import Optional
from .review_result import ReviewResult

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ReviewTask:
    def __init__(self, id: int, repo_url: str, pr_number: int, auth_token: Optional[str], status: TaskStatus, results: Optional[ReviewResult] = None):
        self.id = id
        self.repo_url = repo_url
        self.pr_number = pr_number
        self.auth_token = auth_token
        self.status = status
        self.results = results