
# Exceptions
class UnableToCountCores(BaseException):
    """Unable to automatically find number of cores."""

    pass


class IncorrectNumberOfCores(BaseException):
    """Entered number more than there are cores on computer."""

    pass


class EmptyArchiveError(BaseException):
    """Archive is empty. Nothing to unzip."""

    pass


class AllFilesAreEmpty(BaseException):
    """All files in archive is 0 bytes."""

    pass


class CannotUseZeroCores(BaseException):
    """Number of cores cannot be zero"""

    pass
