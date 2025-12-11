from __future__ import annotations

import random
from typing import Any, Dict, Optional

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import (  # type: ignore[reportPrivateImportUsage]
    Iterator,
    LazyAttribute,
    Sequence,
    SubFactory,
)
from factory.faker import Faker  # type: ignore[reportPrivateImportUsage]
from factory.helpers import lazy_attribute  # type: ignore[reportPrivateImportUsage]

from filare.models.interface.base import FilareInterfaceModel
from filare.models.interface.cable import CableInterfaceModel
from filare.models.interface.connection import (
    ConnectionEndpointInterfaceModel,
    ConnectionInterfaceModel,
    ConnectionWireInterfaceModel,
)
from filare.models.interface.connector import (
    ConnectorInterfaceModel,
    LoopInterfaceModel,
)
from filare.models.interface.harness import HarnessInterfaceModel
from filare.models.interface.metadata import (
    AuthorSignatureInterfaceModel,
    MetadataInterfaceModel,
    RevisionSignatureInterfaceModel,
    TemplateInterfaceModel,
)
from filare.models.interface.options import OptionsInterfaceModel


class FakeInterfaceFactory(Factory):
    """Base factory for interface models with YAML export."""

    class Meta:
        abstract = True

    @classmethod
    def build_yaml(cls, **kwargs) -> str:
        instance: FilareInterfaceModel = cls.build(**kwargs)
        return instance.to_yaml()


class FakeTemplateInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = TemplateInterfaceModel

    name = Faker("word")
    sheetsize = Iterator(["A3", "A4", "Letter"])


class FakeAuthorSignatureInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = AuthorSignatureInterfaceModel

    name = Faker("name")
    date = Faker("date")


class FakeRevisionSignatureInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = RevisionSignatureInterfaceModel

    name = Faker("name")
    date = Faker("date")
    changelog = Faker("sentence")


class FakeMetadataInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = MetadataInterfaceModel

    title = Faker("sentence", nb_words=3)
    pn = Faker("bothify", text="PN-####")
    company = Faker("company")
    address = Faker("address")
    template = SubFactory(FakeTemplateInterfaceFactory)

    @lazy_attribute
    def authors(self) -> Dict[str, AuthorSignatureInterfaceModel]:
        return {
            "created": FakeAuthorSignatureInterfaceFactory.build(),
            "reviewed": FakeAuthorSignatureInterfaceFactory.build(),
        }

    @lazy_attribute
    def revisions(self) -> Dict[str, RevisionSignatureInterfaceModel]:
        return {"a": FakeRevisionSignatureInterfaceFactory.build()}


class FakeOptionsInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = OptionsInterfaceModel

    include_bom = True
    include_cut_diagram = False
    include_termination_diagram = False
    split_bom_page = False
    split_notes_page = False
    split_index_page = False


class FakeLoopInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = LoopInterfaceModel

    first = Iterator([1, 2, "1", "2"])
    second = Iterator([2, 3, "A", "B"])
    side = Iterator([None, "LEFT", "RIGHT"])
    color = Iterator([None, "RD", "GN"])
    show_label = True


class FakeConnectorInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = ConnectorInterfaceModel

    designator = Sequence(lambda n: f"J{n+1}")
    type = Iterator(["D-Sub", "Molex KK 254", "Circular"])
    subtype = Iterator(["female", "male", None])
    pins = LazyAttribute(lambda _: [1, 2, 3])
    pinlabels = LazyAttribute(lambda _: ["1", "2", "3"])
    pincolors = LazyAttribute(lambda _: ["RD", "BK", "GN"])
    loops = LazyAttribute(lambda _: [FakeLoopInterfaceFactory.build()])
    style = Iterator([None, "simple"])


class FakeCableInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = CableInterfaceModel

    designator = Sequence(lambda n: f"W{n+1}")
    wirecount = 3
    colors = LazyAttribute(lambda _: ["RD", "BK", "GN"])
    length = Iterator(["0.5 m", "1 m", None])
    gauge = Iterator(["0.25 mm2", "24 AWG", None])
    shield = Iterator([False, True])
    type = Iterator([None, "CAT5e", "Serial"])


class FakeConnectionEndpointInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = ConnectionEndpointInterfaceModel

    parent = Sequence(lambda n: f"J{n+1}")
    pin = Iterator([1, 2, "1", "2"])


class FakeConnectionWireInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = ConnectionWireInterfaceModel

    parent = Sequence(lambda n: f"W{n+1}")
    wire = Iterator([1, 2, "1", "2"])


class FakeConnectionInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = ConnectionInterfaceModel

    from_ = SubFactory(FakeConnectionEndpointInterfaceFactory)
    via = SubFactory(FakeConnectionWireInterfaceFactory)
    to = SubFactory(FakeConnectionEndpointInterfaceFactory)

    @classmethod
    def build(cls, **kwargs: Any) -> ConnectionInterfaceModel:
        # randomize missing endpoints to allow half-connections in tests
        if "from_" not in kwargs and random.choice([True, False]):
            kwargs["from_"] = None
        if "to" not in kwargs and random.choice([True, False]):
            kwargs["to"] = None
        if kwargs.get("from_") is None and kwargs.get("to") is None:
            kwargs["from_"] = FakeConnectionEndpointInterfaceFactory.build()
        return super().build(**kwargs)


class FakeHarnessInterfaceFactory(FakeInterfaceFactory):
    class Meta:
        model = HarnessInterfaceModel

    metadata = SubFactory(FakeMetadataInterfaceFactory)
    options = SubFactory(FakeOptionsInterfaceFactory)

    @lazy_attribute
    def connectors(self) -> Dict[str, ConnectorInterfaceModel]:
        designators = [f"J{idx + 1}" for idx in range(2)]
        return {
            designator: FakeConnectorInterfaceFactory.build(designator=designator)
            for designator in designators
        }

    @lazy_attribute
    def cables(self) -> Dict[str, CableInterfaceModel]:
        designators = [f"W{idx + 1}" for idx in range(1)]
        return {
            designator: FakeCableInterfaceFactory.build(designator=designator)
            for designator in designators
        }

    @lazy_attribute
    def connections(self) -> list[ConnectionInterfaceModel]:
        connector_ids = list(self.connectors.keys())
        cable_ids = list(self.cables.keys())
        return [
            ConnectionInterfaceModel(
                from_=ConnectionEndpointInterfaceModel(
                    parent=connector_ids[0],
                    pin=1,
                ),
                via=ConnectionWireInterfaceModel(
                    parent=cable_ids[0],
                    wire=1,
                ),
                to=ConnectionEndpointInterfaceModel(
                    parent=connector_ids[-1],
                    pin=2,
                ),
            )
        ]
