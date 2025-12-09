import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class HarnessQuantity(BaseModel):
    """Stores per-harness quantity multipliers and their backing file paths."""

    harnesses: List[Path]
    multiplier_file_name: str = "quantity_multipliers.txt"
    output_dir: Optional[Path] = None
    multipliers: Dict[str, int] = Field(default_factory=dict)
    folder: Path
    qty_multipliers: Path

    def __init__(
        self,
        harnesses,
        multiplier_file_name="quantity_multipliers.txt",
        output_dir=None,
        **data,
    ):
        super().__init__(
            harnesses=list(harnesses),
            multiplier_file_name=multiplier_file_name,
            output_dir=output_dir,
            **data,
        )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def _derive_paths(cls, values):
        """Populate folder and multiplier file path from the first harness file."""
        harnesses = values.get("harnesses") or []
        if not harnesses:
            return values
        folder = values.get("output_dir") or harnesses[0].parent
        values["folder"] = folder
        values["qty_multipliers"] = folder / values.get(
            "multiplier_file_name", "quantity_multipliers.txt"
        )
        return values

    @property
    def harness_names(self):
        """Return the stem names (no extension) for all harness files."""
        return [harness.stem for harness in self.harnesses]

    def __getitem__(self, harness):
        return self.multipliers[harness]

    def fetch_qty_multipliers_from_file(self):
        """Load multipliers from disk or prompt the user if the file is absent."""
        if self.qty_multipliers.is_file():
            with open(self.qty_multipliers, "r") as f:
                try:
                    self.multipliers = json.load(f)
                except json.decoder.JSONDecodeError as err:
                    from filare.errors import FilareToolsException

                    raise FilareToolsException(
                        f"Invalid format for file {self.qty_multipliers}, error: {err}"
                    ) from err
        else:
            self.get_qty_multipliers_from_user()
            self.save_qty_multipliers_to_file()
        self.check_all_multipliers_defined()

    def check_all_multipliers_defined(self):
        for name in self.harness_names:
            if name not in self.multipliers:
                from filare.errors import FilareToolsException

                raise FilareToolsException(
                    f"No multiplier defined for harness {name}, maybe delete the multiplier_file {self.qty_multipliers}"
                )

    def get_qty_multipliers_from_user(self):
        for name in self.harness_names:
            try:
                self.multipliers[name] = int(
                    input("Quantity multiplier for {}? ".format(name))
                )
            except ValueError:
                logging.warning(
                    "Quantity multiplier must be an integer for %s; defaulting to 1",
                    name,
                )
                self.multipliers[name] = 1

    def save_qty_multipliers_to_file(self):
        """Write collected multipliers to the configured JSON file."""
        with open(self.qty_multipliers, "w") as f:
            json.dump(self.multipliers, f)

    def retrieve_harness_qty_multiplier(self, bom_file):
        """Return the multiplier for the harness associated with a BOM file path."""
        return int(self[Path(Path(bom_file).stem).stem])
