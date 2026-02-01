

class GardenException(Exception):
    """Base exception class for all custom exceptions"""
    pass


class RepositoryError(GardenException):
    """Persistence boundary failure."""
    pass