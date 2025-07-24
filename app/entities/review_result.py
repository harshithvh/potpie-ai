"""
Review result, issues, and summary models.
"""

from typing import List

class Issue:
    def __init__(self, type: str, line: int, description: str, suggestion: str, severity: str):
        self.type = type
        self.line = line
        self.description = description
        self.suggestion = suggestion
        self.severity = severity

class FileReview:
    def __init__(self, file_name: str, issues: List[Issue]):
        self.file_name = file_name
        self.issues = issues

class ReviewSummary:
    def __init__(self, total_files: int, total_issues: int, critical_issues: int):
        self.total_files = total_files
        self.total_issues = total_issues
        self.critical_issues = critical_issues

class ReviewResult:
    def __init__(self, files: List[FileReview], summary: ReviewSummary):
        self.files = files
        self.summary = summary