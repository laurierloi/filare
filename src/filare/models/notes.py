import logging
from dataclasses import asdict, dataclass, field, fields
from enum import Enum, IntEnum
from textwrap import dedent
from typing import List

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import LazyAttribute  # type: ignore[reportPrivateImportUsage]
from faker import Faker  # type: ignore[reportPrivateImportUsage]

faker = Faker()


@dataclass
class Notes:
    notes: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.notes, Notes):
            self.notes = self.notes.notes

    def __repr__(self):
        return self.as_html_list()

    def as_html_list(self):
        if self.notes:
            lines = "\n".join(f"  <li>{note}</li>" for note in self.notes)
            return f"<ol>\n{lines}\n</ol>"
        return ""


# TODO: nearly same method is within page_options.py, standardize?
def get_page_notes(parsed_data, page_name: str):
    """Get the page options

    uses: the page\'s notes   -> general notes -> default notes
        ('{page_name}_notes') ->    ('notes')  -> {}
    """
    page_notes_name = f"{page_name}_notes"
    notes = parsed_data.get(page_notes_name, parsed_data.get("notes", []))
    return Notes(notes=notes)


class FakeNotesFactory(Factory):
    """factory_boy factory for Notes dataclass."""

    class Meta:
        model = Notes

    notes = LazyAttribute(lambda _: faker.sentences(nb=3))

    @staticmethod
    def create(**kwargs) -> Notes:
        return FakeNotesFactory.build(**kwargs)


__all__ = ["Notes", "get_page_notes", "FakeNotesFactory"]
