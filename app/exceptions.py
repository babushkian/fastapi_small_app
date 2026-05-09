class NotFoundError(Exception):
    """Resource not found (business-level)."""

class AlreadyExistsError(Exception):
    """Resource conflict / already exists."""

class BusinessError(Exception):
    """Generic business error."""