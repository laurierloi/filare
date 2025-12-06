class FilareBaseException(Exception):
    """Base exception for Filare errors."""


class FilareFlowException(FilareBaseException):
    """Raised for errors in flow/build pipelines."""


class FilareModelException(FilareBaseException):
    """Raised for model/data validation errors."""


class FilareParserException(FilareBaseException):
    """Raised for parsing errors."""


class FilareRenderException(FilareBaseException):
    """Raised for rendering errors."""


class FilareToolsException(FilareBaseException):
    """Raised for tooling/utility errors."""


class MissingOutputSpecification(FilareFlowException):
    """No output formats or return types were provided."""

    def __init__(self) -> None:
        super().__init__("No output formats or return types specified")


class MissingConnectionCountError(FilareFlowException):
    """Connection set lacked any discernible connection count."""

    def __init__(self) -> None:
        super().__init__("No connection count found in connection set")


class RedefinedDesignatorError(FilareFlowException):
    """Raised when a designator is assigned multiple templates."""

    def __init__(
        self, designator: str, previous_template: str, new_template: str
    ) -> None:
        self.designator = designator
        self.previous_template = previous_template
        self.new_template = new_template
        super().__init__(
            f"Trying to redefine {designator} from {previous_template} to {new_template}"
        )


class MultipleSeparatorError(FilareFlowException):
    """Designator contained more than one separator character."""

    def __init__(self, value: str, separator: str, idx: int = None) -> None:
        self.value = value
        self.separator = separator
        suffix = (
            f"connections[{idx}]: entry '{value}' has more than one separator '{separator}'"
            if idx is not None
            else f"{value} - Found more than one separator ({separator})"
        )
        super().__init__(suffix)


class ConnectionCountMismatchError(FilareFlowException):
    """Connection sets referenced differing connection counts."""

    def __init__(self, pretty_sets: str) -> None:
        self.pretty_sets = pretty_sets
        super().__init__(
            "All items in connection set must reference the same number of connections\n"
            f"It is not the case for:{pretty_sets}"
        )


class ComponentTypeMismatch(FilareFlowException):
    """Raised when a designator resolves to an unexpected component type."""

    def __init__(self, expected: str, designator: str, template: str, actual: str):
        self.expected = expected
        self.designator = designator
        self.template = template
        self.actual = actual
        super().__init__(
            f'Expected {expected}, but "{designator}" ("{template}") is {actual}'
        )


class UnknownTemplateDesignator(FilareFlowException):
    """Raised when a template/designator cannot be resolved."""

    def __init__(
        self, template: str, known_connectors: str = "", known_cables: str = ""
    ):
        self.template = template
        suffix = (
            f" (known connectors: {known_connectors or 'none'}; known cables: {known_cables or 'none'})"
        )
        super().__init__(f"Unknown template/designator '{template}'{suffix}")


class InvalidNumberFormat(FilareModelException):
    """Raised when a number/unit string cannot be parsed."""

    def __init__(self, value: str, context: str = ""):
        self.value = value
        self.context = context
        prefix = f"{context}: " if context else ""
        super().__init__(
            f"{prefix}{value} is not a valid number and unit.\n"
            "It must be a number, or a number and unit separated by a space."
        )


class ComponentValidationError(FilareModelException):
    """Generic component/model validation error."""

    def __init__(self, message: str):
        super().__init__(message)


class UnitMismatchError(FilareModelException):
    """Raised when arithmetic is attempted on incompatible units."""

    def __init__(self, left_value, right_value):
        super().__init__(f"Cannot add {left_value} and {right_value}, units not matching")


class CableWireResolutionError(FilareModelException):
    """Raised when a cable wire label/color cannot be resolved uniquely."""

    def __init__(self, cable: str, wire: str, reason: str):
        self.cable = cable
        self.wire = wire
        self.reason = reason
        super().__init__(f"{cable}:{wire} {reason}")


class ColorPaddingUnsupported(FilareModelException):
    """Raised when an unsupported color padding length is requested."""

    def __init__(self, length: int):
        self.length = length
        super().__init__(f"Padding not supported for len {length}")


class FileResolutionError(FilareToolsException, FileNotFoundError):
    """Raised when a file cannot be resolved in allowed search paths."""

    def __init__(self, filename, search_paths):
        self.filename = filename
        self.search_paths = search_paths
        paths_display = (
            "\n".join(str(p) for p in search_paths) if search_paths else str(filename)
        )
        self.message = f"{filename} was not found in: \n{paths_display}"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ViewportParseError(FilareToolsException):
    """Raised when viewport strings cannot be parsed."""

    def __init__(self, value: str):
        super().__init__(f"Viewport must be WIDTHxHEIGHT, e.g., 1280x720 (got {value})")


class UnsupportedLoopSide(FilareRenderException):
    """Raised when loop rendering cannot determine a connector side."""

    def __init__(self, designator: str):
        super().__init__(
            f"Connector {designator}: no side set for loops; set ports_left/ports_right or loop side."
        )


class InvalidSVGRoot(FilareRenderException):
    """Raised when an imported SVG is missing the root <svg> element."""

    def __init__(self, svg_path):
        super().__init__(f"File {svg_path} does not contain a root <svg> element.")


class PinResolutionError(FilareModelException):
    """Raised when a connector pin cannot be resolved from label/number."""

    def __init__(self, connector: str, message: str):
        self.connector = connector
        super().__init__(f"{connector}: {message}")


class MetadataValidationError(FilareModelException):
    """Raised for invalid metadata values."""

    def __init__(self, message: str):
        super().__init__(message)


class PartNumberValidationError(FilareModelException):
    """Raised when part number fields are malformed."""

    def __init__(self, value):
        super().__init__(f"pn ({value}) should not be a list")


class BomEntryHashError(FilareModelException):
    """Raised when BOM entry hashes are not stable."""

    def __init__(self, entry):
        super().__init__(
            f"BomEntry's hash is not persistent: h1:{hash(entry)} h2:{hash(entry)}\n\tentry: {entry}"
        )


class UnsupportedModelOperation(FilareModelException):
    """Raised when a model operation is not supported."""

    def __init__(self, operation: str):
        super().__init__(operation)
