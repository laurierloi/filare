import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import click
from pydantic import BaseModel, Field, ConfigDict, model_validator


class HarnessQuantity(BaseModel):
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
        return [harness.stem for harness in self.harnesses]

    def __getitem__(self, harness):
        return self.multipliers[harness]

    def fetch_qty_multipliers_from_file(self):
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
                from filare.errors import FilareToolsException

                raise FilareToolsException("Quantity multiplier must be an integer!")

    def save_qty_multipliers_to_file(self):
        with open(self.qty_multipliers, "w") as f:
            json.dump(self.multipliers, f)

    def retrieve_harness_qty_multiplier(self, bom_file):
        return int(self[Path(Path(bom_file).stem).stem])


@click.command(no_args_is_help=True)
@click.argument(
    "files",
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=False,
        path_type=Path,
    ),
    nargs=-1,
    required=True,
)
@click.option(
    "-m",
    "--multiplier-file-name",
    default="quantity_multipliers.txt",
    type=str,
    help="name of file used to fetch or save the qty_multipliers",
)
@click.option(
    "-f",
    "--force-new",
    is_flag=True,
    type=bool,
    help="if set, will always ask for new multipliers",
)
def qty_multipliers(files, multiplier_file_name, force_new):
    harnesses = HarnessQuantity(files, multiplier_file_name)
    if force_new:
        harnesses.qty_multipliers.unlink(missing_ok=True)

    harnesses.fetch_qty_multipliers_from_file()
    qty_multipliers = harnesses.multipliers
    return
