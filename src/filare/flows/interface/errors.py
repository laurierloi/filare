from filare.errors import FilareFlowException


class InterfaceFlowError(FilareFlowException):
    """Raised when interface flows encounter invalid or missing data."""
