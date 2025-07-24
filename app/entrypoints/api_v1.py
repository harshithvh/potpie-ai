"""
FastAPI endpoints for PR analysis.
"""

from fastapi import APIRouter
from app.entrypoints.schemas import (
    AnalyzePRRequest, TaskStatusResponse, ReviewResultResponse, ReviewResultModel, FileReviewModel, IssueModel, ReviewSummaryModel
)
from app.core.crud_service import CrudService

def get_router(crud_service: CrudService):
    router = APIRouter()

    @router.get("/health")
    def health_check():
        return {"status": "OK"}

    @router.post("/analyze-pr", response_model=TaskStatusResponse)
    def analyze_pr(request: AnalyzePRRequest):
        task_id = crud_service.create_review_task(request.repo_url, request.pr_number, request.github_token)
        return TaskStatusResponse(task_id=task_id, status="pending")

    @router.get("/status/{task_id}", response_model=TaskStatusResponse)
    def get_status(task_id: int):
        status = crud_service.get_task_status(task_id)
        return TaskStatusResponse(task_id=task_id, status=status)

    @router.get("/results/{task_id}", response_model=ReviewResultResponse)
    def get_results(task_id: int):
        status, results = crud_service.get_task_result(task_id)
        if results is None:
            return ReviewResultResponse(task_id=task_id, status=status, results=None)
        files = [
            FileReviewModel(
                file_name=f.file_name,
                issues=[
                    IssueModel(
                        type=i.type,
                        line=i.line,
                        description=i.description,
                        suggestion=i.suggestion,
                        severity=i.severity
                    ) for i in f.issues
                ]
            ) for f in results.files
        ]
        summary = ReviewSummaryModel(
            total_files=results.summary.total_files,
            total_issues=results.summary.total_issues,
            critical_issues=results.summary.critical_issues
        )
        return ReviewResultResponse(
            task_id=task_id,
            status=status,
            results=ReviewResultModel(files=files, summary=summary)
        )

    return router