"""
Custom exceptions for the application.
"""

class TaskNotFoundException(Exception):
    pass

class InvalidPullRequestException(Exception):
    pass

class LLMServiceException(Exception):
    pass

class ExternalServiceException(Exception):
    pass