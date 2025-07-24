"""
Pull Request domain model.
"""

from typing import List, Optional

class FileChange:
    def __init__(self, file_name: str, patch: str):
        self.file_name = file_name
        self.patch = patch

class PullRequest:
    def __init__(self, repo_url: str, pr_number: int, title: str, description: str, file_changes: List[FileChange]):
        self.repo_url = repo_url
        self.pr_number = pr_number
        self.title = title
        self.description = description
        self.file_changes = file_changes