"""Shared models for additional components/BOM entries."""

from __future__ import annotations

from typing import Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

faker = Faker()


class Quantity(BaseModel):
    """Quantity value with optional unit."""

    number: int = Field(..., description="Quantity number for the component.")
    unit: Optional[str] = Field(default=None, description="Optional quantity unit.")

    model_config = ConfigDict(extra="forbid")


class BomEntry(BaseModel):
    """BOM-style entry for an additional component."""

    qty: Quantity
    description: str = Field(..., description="Description of the additional component.")
    id: Optional[str] = Field(default=None, description="Optional component identifier.")

    model_config = ConfigDict(extra="forbid")


class AdditionalComponent(BaseModel):
    """Wrapper for additional BOM entries."""

    bom_entry: BomEntry

    model_config = ConfigDict(extra="forbid")


class FakeQuantityFactory:
    """faker-backed factory for Quantity."""

    @classmethod
    def create(cls, **overrides: object) -> Quantity:
        payload = {
            "number": faker.random_int(min=1, max=9),
            "unit": faker.random_element(elements=[None, "pcs", "ea"]),
        }
        for key, value in overrides.items():
            payload[key] = value
        return Quantity(**payload)


class FakeBomEntryFactory:
    """faker-backed factory for BomEntry."""

    @classmethod
    def create(cls, **overrides: object) -> BomEntry:
        qty_override = overrides.pop("qty", None)
        payload = {
            "qty": qty_override or FakeQuantityFactory.create(),
            "description": faker.sentence(nb_words=3),
            "id": faker.bothify(text="AC##"),
        }
        for key, value in overrides.items():
            payload[key] = value
        return BomEntry(**payload)


class FakeAdditionalComponentFactory:
    """faker-backed factory for AdditionalComponent."""

    @classmethod
    def create(cls, **overrides: object) -> AdditionalComponent:
        bom_entry_id = overrides.pop("bom_entry_id", None)
        bom_entry = FakeBomEntryFactory.create()
        if bom_entry_id is not None:
            bom_entry.id = str(bom_entry_id)
        clean_overrides = {k: v for k, v in overrides.items() if k != "bom_entry"}
        return AdditionalComponent(bom_entry=bom_entry, **clean_overrides)
