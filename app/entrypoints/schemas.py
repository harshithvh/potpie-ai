"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel
from typing import List, Optional

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: int
    status: str

class IssueModel(BaseModel):
    type: str
    line: int
    description: str
    suggestion: str
    severity: str

class FileReviewModel(BaseModel):
    file_name: str
    issues: List[IssueModel]

class ReviewSummaryModel(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class ReviewResultModel(BaseModel):
    files: List[FileReviewModel]
    summary: ReviewSummaryModel

class ReviewResultResponse(BaseModel):
    task_id: int
    status: str
    results: Optional[ReviewResultModel] = None