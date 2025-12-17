"""Helpers to build Notes template models from explicit inputs."""

from __future__ import annotations

from typing import Optional, Sequence, Union

from filare.models.hypertext import MultilineHypertext
from filare.models.templates.notes_template_model import (
    NotesTemplateModel,
    TemplateNotesOptions,
)


def build_notes_model(
    notes: Union[MultilineHypertext, str, Sequence[str]],
    options: Optional[TemplateNotesOptions] = None,
    **option_overrides: object,
) -> NotesTemplateModel:
    """Construct a NotesTemplateModel from explicit inputs."""
    notes_value = (
        notes if isinstance(notes, MultilineHypertext) else MultilineHypertext.to(notes)
    )
    opts = options or TemplateNotesOptions()
    for key, value in option_overrides.items():
        if hasattr(opts, key):
            setattr(opts, key, value)
    return NotesTemplateModel(notes=notes_value, options=opts)
