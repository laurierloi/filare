# -*- coding: utf-8 -*-

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from graphviz import Graph

from filare import APP_NAME, APP_URL, __version__
from filare.errors import BomEntryHashError
from filare.models import colors
from filare.models.bom import BomContent, BomEntry, BomEntryBase, BomRenderOptions
from filare.models.cable import CableModel
from filare.models.component import ComponentModel
from filare.models.connector import ConnectorModel
from filare.models.document import DocumentRepresentation
from filare.models.metadata import Metadata
from filare.models.notes import Notes
from filare.models.options import PageOptions
from filare.models.types import BomCategory, Side
from filare.render.assets import embed_svg_images, embed_svg_images_file
from filare.render.graphviz import (
    gv_connector_loops,
    gv_edge_wire,
    gv_node_cable,
    gv_node_connector,
    set_dot_basics,
)
from filare.render.html import generate_html_output
from filare.render.imported_svg import prepare_imported_svg
from filare.render.pdf import generate_pdf_output
from filare.render.templates import get_template  # for compatibility with tests
from filare.settings import settings

# Compatibility dataclass aliases
if TYPE_CHECKING:
    from filare.models.dataclasses import Cable as CableDC
    from filare.models.dataclasses import Component as ComponentDC
    from filare.models.dataclasses import Connector as ConnectorDC
else:  # pragma: no cover
    try:
        from filare.models.dataclasses import Cable as CableDC
        from filare.models.dataclasses import Component as ComponentDC
        from filare.models.dataclasses import Connector as ConnectorDC
    except Exception:  # pragma: no cover
        CableDC = ComponentDC = ConnectorDC = None  # type: ignore

Cable = CableDC  # type: ignore
Component = ComponentDC  # type: ignore
Connector = ConnectorDC  # type: ignore


@dataclass
class Harness:
    metadata: Metadata
    options: PageOptions
    notes: Notes
    additional_bom_items: List[Component] = field(default_factory=list)
    shared_bom: Dict = field(default_factory=dict)
    document: Optional[DocumentRepresentation] = None

    def __post_init__(self):
        self.connectors = {}
        self.cables = {}
        self.bom = {}
        self.additional_bom_items = []

    @property
    def name(self) -> str:
        return self.metadata.name

    def add_connector(
        self, designator: Union[str, ConnectorModel, Dict[str, Any]], *args, **kwargs
    ) -> None:
        """Accept dataclass args, ConnectorModel, or mapping and store keyed by designator."""
        if ConnectorDC is None:  # pragma: no cover
            raise TypeError("Connector dataclass not available")
        assert Connector is not None
        if args or kwargs:
            conn = Connector(designator=str(designator), *args, **kwargs)
            key = designator
        elif isinstance(designator, ConnectorModel):
            conn = designator.to_connector()
            key = conn.designator
        elif isinstance(designator, dict):
            conn = Connector(**designator)
            key = conn.designator
        else:
            conn = Connector(designator=designator)
            key = designator
        self.connectors[key] = conn

    def add_connector_model(
        self, connector_model: Union[ConnectorModel, Dict[str, Any]]
    ) -> None:
        """Accept a ConnectorModel (or similar with to_connector()) and store the dataclass."""
        if isinstance(connector_model, dict):
            conn = Connector(**connector_model)
        elif isinstance(connector_model, ConnectorModel):
            conn = connector_model.to_connector()
        else:
            raise TypeError("connector_model must be ConnectorModel or dict")
        self.connectors[conn.designator] = conn

    def add_cable(
        self, designator: Union[str, CableModel, Dict[str, Any]], *args, **kwargs
    ) -> None:
        """Accept dataclass args, CableModel, or mapping and store keyed by designator."""
        if CableDC is None:  # pragma: no cover
            raise TypeError("Cable dataclass not available")
        assert Cable is not None
        if args or kwargs:
            cbl = Cable(designator=str(designator), *args, **kwargs)
            key = designator
        elif isinstance(designator, CableModel):
            cbl = designator.to_cable()
            key = cbl.designator
        elif isinstance(designator, dict):
            cbl = Cable(**designator)
            key = cbl.designator
        else:
            cbl = Cable(designator=designator)
            key = designator
        self.cables[key] = cbl

    def add_cable_model(self, cable_model: Union[CableModel, Dict[str, Any]]) -> None:
        """Accept a CableModel (or similar with to_cable()) and store the dataclass."""
        if isinstance(cable_model, dict):
            cable = Cable(**cable_model)
        elif isinstance(cable_model, CableModel):
            cable = cable_model.to_cable()
        else:
            raise TypeError("cable_model must be CableModel or dict")
        self.cables[cable.designator] = cable

    def add_additional_bom_item(self, item: Union[dict, ComponentModel]) -> None:
        if ComponentDC is None:  # pragma: no cover
            raise TypeError("Component dataclass not available")
        if isinstance(item, ComponentModel):
            new_item = item.to_component()
        else:
            new_item = Component(**item, category=BomCategory.ADDITIONAL)
        self.additional_bom_items.append(new_item)

    def orient_connectors_overview(self):
        """Set connector port orientation based on connection direction for overview mode."""
        if not self.connectors:
            return

        left_side = set()
        right_side = set()

        for cable in self.cables.values():
            for connection in cable._connections:
                if connection.from_ is not None:
                    left_side.add(connection.from_.parent)
                if connection.to is not None:
                    right_side.add(connection.to.parent)

        for designator, connector in self.connectors.items():
            on_left = designator in left_side
            on_right = designator in right_side
            if not (on_left or on_right):
                continue
            connector.ports_right = on_left
            connector.ports_left = on_right

    def populate_bom(self):
        # helper lists
        all_toplevel_items = (
            list(self.connectors.values())
            + list(self.cables.values())
            + self.additional_bom_items
        )
        all_subitems = [
            subitem
            for item in all_toplevel_items
            for subitem in item.additional_components
        ]
        all_bom_relevant_items = (
            list(self.connectors.values())
            + [cable for cable in self.cables.values() if cable.category != "bundle"]
            + [
                wire
                for cable in self.cables.values()
                if cable.category == "bundle"
                for wire in cable.wire_objects.values()
            ]
            + self.additional_bom_items
            + all_subitems
        )

        def add_to_bom(entry):
            if isinstance(entry, list):
                for e in entry:
                    add_to_bom(e)
                return

            def _as_dict(obj):
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                if hasattr(obj, "dict"):
                    return obj.dict()
                return obj

            if not isinstance(entry, BomEntry):
                base = entry
                if isinstance(entry, BomEntryBase):
                    base = entry
                else:
                    maybe_dict = _as_dict(entry)
                    base = BomEntryBase(**maybe_dict)
                entry = BomEntry(
                    qty=base.qty,
                    partnumbers=base.partnumbers,
                    amount=base.amount,
                    qty_multiplier=base.qty_multiplier,
                    description=base.description,
                    category=base.category,
                    designators=list(base.designators),
                    per_harness=dict(base.per_harness),
                    ignore_in_bom=base.ignore_in_bom,
                    id=base.id,
                )

            if isinstance(entry, list):
                for e in entry:
                    add_to_bom(e)
                return

            if hash(entry) in self.bom:
                self.bom[hash(entry)] += entry
            else:
                self.bom[hash(entry)] = entry

            try:
                self.bom[hash(entry)]
            except KeyError:
                raise BomEntryHashError(entry)

        # add items to BOM
        for item in all_bom_relevant_items:
            if item.ignore_in_bom:
                continue
            add_to_bom(item.bom_entry)

        # sort BOM by category first, then alphabetically by description within category
        self.bom = dict(
            sorted(
                self.bom.items(),
                key=lambda x: (
                    x[1].category,
                    x[1].description,
                ),  # x[0] = key, x[1] = value
            )
        )

        next_id = len(self.shared_bom) + 1

        def get_per_harness(v):
            d = {
                "qty": v["qty"],
            }
            return (self.name, d)

        for key, values in self.bom.items():
            if key in self.shared_bom:
                existing = self.shared_bom[key]
                existing.qty += values.qty
                values.id = existing.id
            else:
                values.id = next_id
                self.shared_bom[key] = values
                existing = values
                next_id += 1

            k, v = get_per_harness({"qty": values.qty})
            existing.per_harness[k] = v

        # set BOM IDs within components (for BOM bubbles)
        for item in all_bom_relevant_items:
            if item.ignore_in_bom:
                continue
            if hash(item) not in self.bom:
                continue
            item.id = self.bom[hash(item)].id

        self.bom = dict(
            sorted(
                self.bom.items(),
                key=lambda x: (x[1].id,),
            )
        )

    def connect(
        self,
        from_name: str,
        from_pin: Union[int, str],
        via_name: str,
        via_wire: Union[int, str],
        to_name: str,
        to_pin: Union[int, str],
    ) -> None:
        def clean_pin(pin):
            """Allow for a pin of the form "PINLABEL__PINNUMBER"

            This is a bit treacherous, because we actually allow PINNUMBER which are not int.
            When this happens, the pinnumber will be considered as a pinlabel.
            The logic below should handle that case

            """
            pinlabel = None
            pinnumber = None
            if isinstance(pin, str):
                if "__" in pin:
                    pinlabel, pinnumber = pin.split("__")
                    pinnumber = int(pinnumber)
                else:
                    try:
                        pinnumber = int(pin)
                    except ValueError:
                        pinlabel = pin
            if isinstance(pin, int):
                pinnumber = pin
            return pinlabel, pinnumber

        # check from and to connectors
        for name, (pinlabel, pinnumber) in zip(
            [from_name, to_name], [clean_pin(from_pin), clean_pin(to_pin)]
        ):
            if name is None or name not in self.connectors:
                continue

            connector = self.connectors[name]

            pinlabel_indexes = None
            pinnumber_index = None

            if pinlabel is not None:
                pinlabel_indexes = [
                    i for i, x in enumerate(connector.pinlabels) if x == pinlabel
                ]
                if len(pinlabel_indexes) == 0:
                    pinlabel_indexes = None
                    if pinlabel in connector.pins:
                        pinnumber = pinlabel
                    else:
                        from filare.errors import PinResolutionError

                        raise PinResolutionError(
                            name, f"Pinlabel {pinlabel} is not in pinlabels"
                        )

            if pinnumber is not None:
                pinnumber_indexes = [
                    i for i, x in enumerate(connector.pins) if x == pinnumber
                ]
                if len(pinnumber_indexes) > 1:
                    from filare.errors import PinResolutionError

                    raise PinResolutionError(
                        name, f"Pinnumber {pinnumber} is not unique in pins"
                    )
                pinnumber_index = pinnumber_indexes[0]
                if pinlabel_indexes is not None:
                    if pinnumber_index not in pinlabel_indexes:
                        from filare.errors import PinResolutionError

                        raise PinResolutionError(
                            name,
                            f"No pinnumber {pinnumber} matches pinlabel {pinlabel}; pinlabel for that pinnumber is {connector.pinlabels[pinnumber_index]}",
                        )
            elif pinlabel_indexes is not None:
                if len(pinlabel_indexes) > 1:
                    pinnumber_indexes = [connector.pins[i] for i in pinlabel_indexes]
                    from filare.errors import PinResolutionError

                    raise PinResolutionError(
                        name,
                        f"Pinlabel {pinlabel} is not unique in pinlabels (available pins are: {pinnumber_indexes}), and no pinnumber defined to disambiguate",
                    )
                pinnumber_index = pinlabel_indexes[0]

            if pinnumber_index is None:
                from filare.errors import PinResolutionError

                raise PinResolutionError(
                    name,
                    f"Neither pinlabel ({pinlabel}) or pinnumber ({pinnumber}) were found; pinlabels: {connector.pinlabels}, pinnumbers: {connector.pins}",
                )

            pin = connector.pins[pinnumber_index]
            if name == from_name:
                from_pin = pin
            if name == to_name:
                to_pin = pin

        # check via cable
        if via_name in self.cables:
            cable = self.cables[via_name]
            # check if provided name is ambiguous
            if via_wire in cable.colors and via_wire in cable.wirelabels:
                if cable.colors.index(via_wire) != cable.wirelabels.index(via_wire):
                    from filare.errors import CableWireResolutionError

                    raise CableWireResolutionError(
                        via_name,
                        str(via_wire),
                        "is defined both in colors and wirelabels, for different wires.",
                    )
                # TODO: Maybe issue a warning if present in both lists
                # but referencing the same wire?
            if via_wire in cable.colors:
                if cable.colors.count(via_wire) > 1:
                    from filare.errors import CableWireResolutionError

                    raise CableWireResolutionError(
                        via_name, str(via_wire), "is used for more than one wire."
                    )
                # list index starts at 0, wire IDs start at 1
                via_wire = cable.colors.index(via_wire) + 1
            elif via_wire in cable.wirelabels:
                if cable.wirelabels.count(via_wire) > 1:
                    from filare.errors import CableWireResolutionError

                    raise CableWireResolutionError(
                        via_name, str(via_wire), "is used for more than one wire."
                    )
                via_wire = (
                    cable.wirelabels.index(via_wire) + 1
                )  # list index starts at 0, wire IDs start at 1

        # perform the actual connection
        if from_name and from_name in self.connectors:
            from_con = self.connectors[from_name]
            from_pin_obj = from_con.pin_objects[from_pin]
        else:
            from_pin_obj = None
        if to_name and to_name in self.connectors:
            to_con = self.connectors[to_name]
            to_pin_obj = to_con.pin_objects[to_pin]
        else:
            to_pin_obj = None

        try:
            self.cables[via_name]._connect(from_pin_obj, via_wire, to_pin_obj)
        except Exception as e:
            logging.warning(
                f"fail to connect cable {via_name}, from_pin: {from_pin}, via_wire: {via_wire}, to_pin: {to_pin}\n\texception:{e}"
            )
            raise
        if from_name in self.connectors:
            self.connectors[from_name].activate_pin(from_pin, Side.RIGHT)
        if to_name in self.connectors:
            self.connectors[to_name].activate_pin(to_pin, Side.LEFT)

    def connect_model(self, connection) -> None:
        """Accept a ConnectionModel (or dict) and route through connect()."""
        from filare.models.connections import ConnectionModel
        from filare.models.dataclasses import Connection as ConnectionDataclass

        if isinstance(connection, dict):
            connection = ConnectionModel(**connection)
        if isinstance(connection, ConnectionModel):
            connection = connection.to_connection()
        if not isinstance(connection, ConnectionDataclass):
            raise TypeError("connection must be ConnectionModel, dict, or Connection")

        from_name = (
            getattr(connection.from_, "parent", None) if connection.from_ else ""
        )
        to_name = getattr(connection.to, "parent", None) if connection.to else ""
        via_name = getattr(connection.via, "parent", None) if connection.via else ""

        from_pin = getattr(connection.from_, "id", None) or getattr(
            connection.from_, "label", ""
        )
        to_pin = getattr(connection.to, "id", None) or getattr(
            connection.to, "label", ""
        )
        via_wire = getattr(connection.via, "id", None) or getattr(
            connection.via, "label", ""
        )

        self.connect(
            str(from_name or ""),
            str(from_pin or ""),
            str(via_name or ""),
            str(via_wire or ""),
            str(to_name or ""),
            str(to_pin or ""),
        )

    def create_graph(self) -> Graph:
        dot = Graph(engine=settings.graphviz_engine or "dot")
        set_dot_basics(dot, self.options)

        for connector in self.connectors.values():
            template_html = gv_node_connector(connector)
            dot.node(
                connector.designator,
                label=f"<\n{template_html}\n>",
                shape="box",
                style="filled",
            )
            if len(connector.loops) > 0:
                loops = gv_connector_loops(connector)
                for loop, head, tail in loops:
                    dot.edge(head, tail, xlabel=loop.label, color=loop.html_color())

        wire_is_multicolor = [
            len(wire.color) > 1
            for cable in self.cables.values()
            for wire in cable.wire_objects.values()
        ]
        if any(wire_is_multicolor):
            colors.padding_amount = 3
        else:
            colors.padding_amount = 1

        for cable in self.cables.values():
            template_html = gv_node_cable(cable)
            style = "filled,dashed" if cable.category == "bundle" else "filled"
            dot.node(
                cable.designator,
                label=f"<\n{template_html}\n>",
                shape="box",
                style=style,
            )

            for connection in cable._connections:
                color, l1, l2, r1, r2 = gv_edge_wire(self, cable, connection)
                dot.attr("edge", color=color)
                if l1 is not None and l2 is not None:
                    dot.edge(l1, l2)
                if r1 is not None and r2 is not None:
                    dot.edge(r1, r2)

        return dot

    _graph = None

    @property
    def graph(self):
        if not self._graph:
            self._graph = self.create_graph()
        return self._graph

    @property
    def png(self):
        from io import BytesIO

        graph = self.graph
        data = BytesIO()
        data.write(graph.pipe(format="png"))
        data.seek(0)
        return data.read()

    @property
    def svg(self):
        diagram_svg_options = getattr(self.options, "diagram_svg", None)
        if diagram_svg_options:
            return prepare_imported_svg(diagram_svg_options)
        graph = self.graph
        return embed_svg_images(graph.pipe(format="svg").decode("utf-8"), Path.cwd())

    def output(
        self,
        filename: Union[str, Path],
        view: bool = False,
        cleanup: bool = True,
        fmt: Sequence[str] = ("html", "png", "svg", "tsv"),
    ) -> None:
        fmt_list = list(fmt)
        imported_svg_markup = None
        diagram_svg_options = getattr(self.options, "diagram_svg", None)
        if diagram_svg_options:
            imported_svg_markup = prepare_imported_svg(diagram_svg_options)
            if "png" in fmt_list:
                logging.info(
                    "diagram_svg set; skipping PNG generation (SVG/HTML will use imported asset)"
                )
                fmt_list = [f for f in fmt_list if f != "png"]

        graph = self.graph
        rendered = set()
        filename_path = Path(filename)
        for f in fmt_list:
            if f in ("png", "svg", "html"):
                render_format = "svg" if f == "html" else f
                if render_format in rendered:
                    continue
                graph.format = render_format
                graph.render(filename=filename_path, view=view, cleanup=cleanup)
                rendered.add(render_format)
        if "svg" in fmt_list or "html" in fmt_list:
            if imported_svg_markup:
                filename_path.with_suffix(".svg").write_text(imported_svg_markup)
            else:
                embed_svg_images_file(filename_path.with_suffix(".svg"))
        if "gv" in fmt_list:
            graph.save(filename=filename_path.with_suffix(".gv"))
        if "tsv" in fmt_list and self.options.include_bom:
            bom_render = BomContent(self.bom).get_bom_render(
                options=BomRenderOptions(
                    restrict_printed_lengths=False,
                )
            )
            filename_path.with_suffix(".tsv").open("w").write(bom_render.as_tsv())
        if "csv" in fmt_list:
            print("CSV output is not yet supported")
        if "html" in fmt_list:
            bom_for_html = self.bom if self.options.include_bom else {}
            rendered = {}
            if imported_svg_markup:
                rendered["diagram"] = imported_svg_markup
            if getattr(self.options, "include_cut_diagram", False):
                cut_rows, cut_html = _build_cut_table(self)
                rendered["cut_rows"] = cut_rows
                rendered["cut_table"] = cut_html
            if getattr(self.options, "include_termination_diagram", False):
                term_rows, term_html = _build_termination_table(self)
                rendered["termination_rows"] = term_rows
                rendered["termination_table"] = term_html
            generate_html_output(
                filename_path,
                bom_for_html,
                self.metadata,
                self.options,
                self.notes,
                rendered,
            )
        if "pdf" in fmt_list:
            generate_pdf_output([filename_path])
        if "html" in fmt_list and "svg" not in fmt_list:
            filename_path.with_suffix(".svg").unlink()


__all__ = ["Harness"]


def _build_cut_table(harness):
    """Build cut table rows and HTML from harness wires."""
    rows = []
    for cable in harness.cables.values():
        seen = set()
        for idx, wire in cable.wire_objects.items():
            if idx in seen:
                continue
            seen.add(idx)
            try:
                wire_suffix = int(idx) + 1
            except (TypeError, ValueError):
                wire_suffix = idx
            color = (
                getattr(wire.color, "code_en", None)
                or getattr(wire.color, "html", "")
                or ",".join(wire.color)
                if hasattr(wire, "color")
                else ""
            )
            length = getattr(wire, "length", None) or getattr(cable, "length", "")
            rows.append(
                {
                    "wire": f"{cable.designator}-{wire_suffix}",
                    "partno": getattr(cable, "pn", "") or "",
                    "color": color or "",
                    "length": length or "",
                }
            )
    from filare.flows.templates import build_cut_table_model

    try:
        tpl = globals().get("get_template")
        if tpl is None:
            raise RuntimeError("get_template not available")
        tpl = tpl("cut_table", ".html")
        return rows, tpl.render({"rows": rows})
    except Exception:
        model = build_cut_table_model(rows)
        return rows, model.render()


def _build_termination_table(harness):
    """Build termination table rows and HTML from harness connections."""
    rows = []
    for cable in harness.cables.values():
        for connection in getattr(cable, "_connections", []):
            src = str(connection.from_.parent) if connection.from_ else ""
            tgt = str(connection.to.parent) if connection.to else ""
            src_term = getattr(connection.from_, "termination", "") or "n/a"
            tgt_term = getattr(connection.to, "termination", "") or "n/a"
            rows.append(
                {
                    "source": src,
                    "target": tgt,
                    "source_termination": src_term,
                    "target_termination": tgt_term,
                }
            )
    from filare.flows.templates import build_termination_table_model

    try:
        tpl = globals().get("get_template")
        if tpl is None:
            raise RuntimeError("get_template not available")
        tpl = tpl("termination_table", ".html")
        return rows, tpl.render({"rows": rows})
    except Exception:
        model = build_termination_table_model(rows)
        return rows, model.render()
