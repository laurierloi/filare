from __future__ import annotations

from typing import Mapping, Optional, Set

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.cable import CableInterfaceModel
from filare.models.interface.connection import ConnectionInterfaceModel
from filare.models.interface.connector import ConnectorInterfaceModel


def _known_pins(connector: ConnectorInterfaceModel) -> Set[str]:
    pins: Set[str] = set()
    pins.update(str(pin) for pin in connector.pins)
    pins.update(str(label) for label in connector.pinlabels)
    return pins


def _validate_endpoint(
    endpoint_name: str,
    endpoint,
    connectors: Mapping[str, ConnectorInterfaceModel],
    connection_key: str,
) -> None:
    if endpoint is None:
        return
    if endpoint.parent not in connectors:
        raise InterfaceFlowError(
            f"Connection '{connection_key}': endpoint '{endpoint_name}' "
            f"references unknown connector '{endpoint.parent}'."
        )
    known = _known_pins(connectors[endpoint.parent])
    if known and str(endpoint.pin) not in known:
        raise InterfaceFlowError(
            f"Connection '{connection_key}': endpoint '{endpoint_name}' pin '{endpoint.pin}' "
            f"is not in connector '{endpoint.parent}' pins {sorted(known)}."
        )


def _validate_via(
    via,
    cables: Mapping[str, CableInterfaceModel],
    connection_key: str,
) -> None:
    if via.parent not in cables:
        raise InterfaceFlowError(
            f"Connection '{connection_key}': via references unknown cable '{via.parent}'."
        )
    cable = cables[via.parent]
    if isinstance(via.wire, int):
        if via.wire < 1 or via.wire > cable.wirecount:
            raise InterfaceFlowError(
                f"Connection '{connection_key}': wire index {via.wire} "
                f"outside cable '{via.parent}' wirecount {cable.wirecount}."
            )
    elif isinstance(via.wire, str) and via.wire.isdigit():
        as_int = int(via.wire)
        if as_int < 1 or as_int > cable.wirecount:
            raise InterfaceFlowError(
                f"Connection '{connection_key}': wire index {via.wire} "
                f"outside cable '{via.parent}' wirecount {cable.wirecount}."
            )


def validate_connection_context(
    connection: ConnectionInterfaceModel,
    key: str,
    connectors: Optional[Mapping[str, ConnectorInterfaceModel]] = None,
    cables: Optional[Mapping[str, CableInterfaceModel]] = None,
) -> None:
    """Validate a connection against provided connector/cable context."""
    if connectors:
        _validate_endpoint("from", connection.from_, connectors, key)
        _validate_endpoint("to", connection.to, connectors, key)
    if cables:
        _validate_via(connection.via, cables, key)
