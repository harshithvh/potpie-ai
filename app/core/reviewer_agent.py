"""
Reviewer agent logic for analyzing pull requests using LLMs.
"""

from typing import List
from pydantic import BaseModel, Field
from app.interfaces.reviewer import IReviewerAgent
from app.interfaces.ai_model import ILanguageModel
from app.entities.pr import PullRequest
from app.entities.review_result import ReviewResult, FileReview, Issue, ReviewSummary


class CodeIssue(BaseModel):
    line_number: int = Field(..., description="Line number where the issue was found")
    type: str = Field(..., description="Type of issue: bug, style, performance, suggestion")
    description: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggestion to fix the issue")
    severity: str = Field(..., description="Severity: low, medium, high, critical")


class FileReviewResponse(BaseModel):
    issues: List[CodeIssue] = Field(default_factory=list, description="List of detected issues")


def get_system_prompt() -> str:
    return """
You are CodeSage, an expert AI code reviewer.
Review the given code diff and provide constructive feedback.
Focus on new code (lines starting with '+').
Only respond with issues if you find any.
Be concise and actionable in your feedback.

Code diff format:
- Lines starting with '+' are new code (focus here)
- Lines starting with '-' are removed code  
- Lines with no prefix are unchanged code
- Each line has a line number at the start
"""


def get_user_prompt(pr_title: str, pr_description: str, patch: str) -> str:
    return f"""
Pull Request Title:
{pr_title}

Description:
{pr_description}

Code Diff:
{patch}
"""


class ReviewerAgent(IReviewerAgent):
    """
    Main agent for reviewing pull requests.
    """
    def __init__(self, llm: ILanguageModel):
        self.llm = llm

    def review_pr(self, pr: PullRequest) -> ReviewResult:
        file_reviews: List[FileReview] = []
        total_files = 0
        total_issues = 0
        critical_issues = 0

        for file in pr.file_changes:
            file_review = self.llm.sync_prompt(
                get_system_prompt(),
                get_user_prompt(pr.title, pr.description, file.patch),
                response_type=FileReviewResponse,
            )

            issues: List[Issue] = []
            for code_issue in file_review.issues:
                issue = Issue(
                    type=code_issue.type,
                    line=code_issue.line_number,
                    description=code_issue.description,
                    suggestion=code_issue.suggestion,
                    severity=code_issue.severity,
                )
                issues.append(issue)
                total_issues += 1
                if issue.severity == "critical":
                    critical_issues += 1

            if issues:
                total_files += 1
            
            file_reviews.append(FileReview(file_name=file.file_name, issues=issues))

        summary = ReviewSummary(total_files, total_issues, critical_issues)
        return ReviewResult(files=file_reviews, summary=summary)