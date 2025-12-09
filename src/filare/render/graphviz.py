# -*- coding: utf-8 -*-

import logging
import re
from pathlib import Path
from typing import Any, List, Optional, Union

from filare import APP_NAME, APP_URL, __version__
from filare.errors import UnsupportedLoopSide
from filare.models.colors import MultiColor, SingleColor
from filare.models.dataclasses import (
    Cable,
    Component,
    Connector,
    ShieldClass,
    WireClass,
)
from filare.models.image import Image
from filare.models.types import Side
from filare.models.utils import html_line_breaks, remove_links
from filare.render.html_utils import Img, Table, Td, Tr
from filare.render.templates import get_template
from filare.settings import settings


def gv_node_connector(connector: Connector) -> Table:
    """Render a connector node as an HTML-like table for Graphviz."""
    # TODO: extend connector style support
    params = {"component": connector, "suppress_images": True}
    is_simple_connector = connector.style == "simple"
    template_name = "connector.html"
    if is_simple_connector:
        template_name = "simple-connector.html"

    rendered = get_template(template_name).render(params)
    cleaned_render = "\n".join([l.rstrip() for l in rendered.split("\n") if l.strip()])
    return cleaned_render


def gv_node_cable(cable: Cable) -> Table:
    """Render a cable node as an HTML-like table for Graphviz."""
    # TODO: support multicolor cables
    # TODO: extend cable style support
    params = {"component": cable, "suppress_images": True}
    template_name = "cable.html"
    rendered = get_template(template_name).render(params)
    cleaned_render = "\n".join([l.rstrip() for l in rendered.split("\n") if l.strip()])
    return cleaned_render


def _node_image_attrs(image: Optional[Image]) -> dict:
    """Build Graphviz image attributes for a node image, resolving paths."""
    if not image:
        return {}
    src_path = Path(image.src)
    if not src_path.is_absolute():
        src_path = (Path.cwd() / src_path).resolve()
    attrs = {"image": str(src_path)}
    # Graphviz imagescale accepts: true, width, height, both, none
    if image.scale:
        attrs["imagescale"] = str(image.scale).lower()
    if image.fixedsize:
        attrs["fixedsize"] = "true"
    return attrs


def gv_connector_loops(connector: Connector) -> List:
    """Return loop edges for a connector with placement hints."""
    loop_edges = []
    if connector.ports_left:
        loop_side = "l"
        loop_dir = "w"
    elif connector.ports_right:
        loop_side = "r"
        loop_dir = "e"
    else:
        raise UnsupportedLoopSide(connector.designator)
    for loop in connector.loops:
        this_loop_side = loop_side
        this_loop_dir = loop_dir
        if loop.side == Side.RIGHT:
            this_loop_side = "r"
            this_loop_dir = "e"
        elif loop.side == Side.LEFT:
            this_loop_side = "l"
            this_loop_dir = "w"

        head = (
            f"{connector.designator}:p{loop.first.pin}{this_loop_side}:{this_loop_dir}"
        )
        tail = (
            f"{connector.designator}:p{loop.second.pin}{this_loop_side}:{this_loop_dir}"
        )
        loop_edges.append((loop, head, tail))
    return loop_edges


def gv_edge_wire(harness, cable, connection) -> (str, str, str):
    """Return Graphviz edge descriptors for a connection through a wire/shield."""
    if connection.via.color:
        # check if it's an actual wire and not a shield
        color = f"#000000:{connection.via.color.html_padded}:#000000"
    else:  # it's a shield connection
        color = "#000000"

    if connection.from_ is not None:  # connect to left
        from_port_str = (
            f":p{connection.from_.index+1}r"
            if harness.connectors[str(connection.from_.parent)].style != "simple"
            else ""
        )
        code_left_1 = f"{str(connection.from_.parent)}{from_port_str}:e"
        code_left_2 = f"{str(connection.via.parent)}:w{connection.via.index+1}:w"
        # ports in GraphViz are 1-indexed for more natural maping to pin/wire numbers
    else:
        code_left_1, code_left_2 = None, None

    if connection.to is not None:  # connect to right
        to_port_str = (
            f":p{connection.to.index+1}l"
            if harness.connectors[str(connection.to.parent)].style != "simple"
            else ""
        )
        code_right_1 = f"{str(connection.via.parent)}:w{connection.via.index+1}:e"
        code_right_2 = f"{str(connection.to.parent)}{to_port_str}:w"
    else:
        code_right_1, code_right_2 = None, None

    return color, code_left_1, code_left_2, code_right_1, code_right_2


def set_dot_basics(dot, options):
    logging.debug(
        "Configuring Graphviz graph (engine=%s, font=%s, bgcolor=%s)",
        settings.graphviz_engine,
        getattr(options, "fontname", None),
        getattr(options.bgcolor, "html", options.bgcolor),
    )

    def _coerce_color(value):
        if isinstance(value, dict):
            html = value.get("html") or value.get("code_en") or value
            return SingleColor(html)
        if hasattr(value, "html"):
            return value
        return SingleColor(value)

    dot.body.append(f"// Graph generated by {APP_NAME} {__version__}\n")
    dot.body.append(f"// {APP_URL}\n")
    if settings.graphviz_engine:
        dot.engine = settings.graphviz_engine
    bgcolor = _coerce_color(options.bgcolor)
    bgcolor_node = _coerce_color(options.bgcolor_node)
    dot.attr(
        "graph",
        rankdir="LR",
        ranksep="3",  # TODO: make conditional on the number of components/connections
        bgcolor=bgcolor.html,
        nodesep="0.33",
        fontname=options.fontname,
        splines="polyline",
    )
    dot.attr(
        "node",
        shape="none",
        width="0",
        height="0",
        margin="0",  # Actual size of the node is entirely determined by the label.
        style="filled",
        fillcolor=bgcolor_node.html,
        fontname=options.fontname,
    )
    dot.attr("edge", style="bold", fontname=options.fontname)
