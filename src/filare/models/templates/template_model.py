# pyright: ignore-all
"""Base template model and lightweight factory."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel, ConfigDict


class TemplateModel(BaseModel):
    """Base model for template contexts."""

    template_name: ClassVar[str] = "template"
    model_config = ConfigDict(extra="forbid")

    def to_render_dict(self) -> Dict[str, Any]:
        """Return a dict compatible with template rendering."""
        payload = self.model_dump()
        payload["template_name"] = self.template_name
        return payload

    def render(self) -> str:
        """Render this template model using its template_name."""
        from filare.render.templates import get_template

        return get_template(f"{self.template_name}.html").render(self.to_render_dict())


class TemplateModelFactory:
    """Minimal factory-style helper aligned with factory_boy semantics."""

    class Meta:
        model = TemplateModel

    def __init__(self, **kwargs: Any):
        self._kwargs = kwargs
        self._instance: TemplateModel | None = None

    @classmethod
    def create(cls, **kwargs: Any) -> TemplateModel:
        return cls(**kwargs)._build()

    def _build(self) -> TemplateModel:
        model_class: Type[TemplateModel] = self.Meta.model  # type: ignore[attr-defined]
        return model_class(**self._kwargs)

    def __call__(self) -> Any:
        return self._build()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to a built model for convenience."""
        if name.startswith("_"):
            raise AttributeError(name)
        if self._instance is None:
            self._instance = self._build()
        return getattr(self._instance, name)
