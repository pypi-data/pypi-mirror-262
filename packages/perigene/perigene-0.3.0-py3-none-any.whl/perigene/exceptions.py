class MissingTargetDataException(Exception):
    """
    Raised when attempting to access test data for a model that has none.
    """


class MissingColumnException(Exception):
    """
    Raised when a required column is missing from a data file.
    """


class MissingInfoParamException(Exception):
    pass


class InvalidRegionException(Exception):
    """Raised when a region is invalid."""
