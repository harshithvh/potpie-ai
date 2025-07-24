"""
Adapter for fetching pull request data from GitHub.
"""

import re
from typing import List
from logging import Logger
from github import Github, Auth
from app.entities.pr import PullRequest, FileChange
from app.interfaces.pr_repo import IPullRequestRepo

MAX_FILE_PATCH_SIZE = 5000


def extract_line_number(patch: str) -> int:
    """Extract starting line number from patch header."""
    match = re.search(r"@@ -\s*(\d+)", patch)
    return int(match.group(1)) if match else 1


def add_line_numbers_to_patch(patch: str, start_line: int) -> str:
    """Add line numbers to patch for better context."""
    lines = patch.splitlines()
    numbered_lines = []
    current_line = start_line
    
    for line in lines:
        if not line.startswith("-"):  # Skip deleted lines
            numbered_lines.append(f"{current_line}. {line}")
            current_line += 1
        else:
            numbered_lines.append(line)
    
    return "\n".join(numbered_lines)


class GithubPRGateway(IPullRequestRepo):
    def __init__(self, github_token: str = None, logger: Logger = None):
        self.github_token = github_token
        self.logger = logger
        
        # Initialize GitHub client with auth if token is available
        if github_token:
            auth = Auth.Token(github_token)
            self.github = Github(auth=auth)
        else:
            self.github = Github()  # Public access only

    def _parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Parse GitHub repo URL to extract owner and repo name."""
        parts = repo_url.split("github.com/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub repo URL")
        
        path_parts = parts[1].strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repo URL format")
        
        return path_parts[0], path_parts[1]

    def get(self, repo_url: str, pr_number: int, auth_token: str = None) -> PullRequest:
        owner, repo_name = self._parse_repo_url(repo_url)
        
        # Use provided auth token if available, otherwise use default
        github_client = self.github
        if auth_token and auth_token != self.github_token:
            auth = Auth.Token(auth_token)
            github_client = Github(auth=auth)
        
        if self.logger:
            self.logger.info(f"Fetching PR #{pr_number} from {owner}/{repo_name}")

        try:
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            
            title = pr.title or ""
            description = pr.body or ""
            
            if self.logger:
                self.logger.info(f"Fetched PR details: '{title}'")

            # Get file changes
            file_changes: List[FileChange] = []
            files = pr.get_files()
            
            for file_data in files:
                file_name = file_data.filename
                patch = file_data.patch
                
                # Skip files without patches
                if not patch:
                    if self.logger:
                        self.logger.debug(f"Skipping file '{file_name}' - no patch available")
                    continue
                
                # Skip very large patches
                if len(patch) > MAX_FILE_PATCH_SIZE:
                    if self.logger:
                        self.logger.debug(f"Skipping file '{file_name}' - patch too large ({len(patch)} chars)")
                    continue
                
                # Add line numbers to patch for better context
                start_line = extract_line_number(patch)
                numbered_patch = add_line_numbers_to_patch(patch, start_line)
                
                file_changes.append(FileChange(file_name, numbered_patch))
            
            if self.logger:
                self.logger.info(f"Processed {len(file_changes)} files from PR #{pr_number}")

            return PullRequest(repo_url, pr_number, title, description, file_changes)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error fetching PR #{pr_number} from {owner}/{repo_name}: {e}")
            raise