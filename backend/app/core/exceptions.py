class PromptMasterError(Exception):
    """Base exception for backend errors."""


class ConfigurationError(PromptMasterError):
    """Raised when required application configuration is missing."""
