"""
Interface for pull request repository (GitHub, etc).
"""

from app.entities.pr import PullRequest

class IPullRequestRepo:
    def get(self, repo_url: str, pr_number: int, auth_token: str = None) -> PullRequest:
        raise NotImplementedError