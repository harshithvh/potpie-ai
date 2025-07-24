"""
Interface for reviewer agent.
"""

from app.entities.pr import PullRequest
from app.entities.review_result import ReviewResult

class IReviewerAgent:
    def review_pr(self, pr: PullRequest) -> ReviewResult:
        raise NotImplementedError