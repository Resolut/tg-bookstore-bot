class BookstoreException(Exception):
    """Base exception for the bookstore application."""

    pass


class DatabaseError(BookstoreException):
    """Raised when there is a database-related error."""

    pass


class ValidationError(BookstoreException):
    """Raised when there is a validation error."""

    pass


class NotFoundError(BookstoreException):
    """Raised when a requested resource is not found."""

    pass


class PermissionError(BookstoreException):
    """Raised when a user doesn't have permission to perform an action."""

    pass


class BusinessLogicError(BookstoreException):
    """Raised when there is a business logic error."""

    pass
