"""Domain models for connectors, cables, BOM, metadata, and related helpers."""

from filare.models.bom import *  # noqa: F401,F403
from filare.models.cable import *  # noqa: F401,F403
from filare.models.colors import *  # noqa: F401,F403
from filare.models.component import *  # noqa: F401,F403
from filare.models.configs import *  # noqa: F401,F403
from filare.models.connections import *  # noqa: F401,F403
from filare.models.connector import *  # noqa: F401,F403

# Keep key dataclasses for compatibility
from filare.models.dataclasses import (  # noqa: F401
    Cable,
    Component,
    Connection,
    Connector,
    GraphicalComponent,
    Loop,
    PinClass,
    ShieldClass,
    WireClass,
)
from filare.models.document import *  # noqa: F401,F403
from filare.models.harness import *  # noqa: F401,F403
from filare.models.harness_quantity import *  # noqa: F401,F403
from filare.models.metadata import *  # noqa: F401,F403
from filare.models.options import *  # noqa: F401,F403
from filare.models.page import *  # noqa: F401,F403
from filare.models.primitives import *  # noqa: F401,F403
from filare.models.table_models import *  # noqa: F401,F403
from filare.models.template_inputs import *  # noqa: F401,F403
from filare.models.termination import *  # noqa: F401,F403
from filare.models.types import *  # noqa: F401,F403
from filare.models.wire import *  # noqa: F401,F403
