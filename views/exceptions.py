__all__ = ["WindowingIndexError"]


class WindowingIndexError(LookupError):
    """Raised when a windowing index is out of range"""
    pass
