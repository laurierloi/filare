import logging
from dataclasses import asdict, dataclass, field, fields
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Union

from filare.models.harness_quantity import HarnessQuantity
from filare.models.metadata import PagesMetadata
from filare.models.table_models import letter_suffix
from filare.render.templates import get_template

TABLE_COLUMNS = ["sheet", "page", "quantity", "notes"]


@dataclass(frozen=True)
class IndexTableRow:
    sheet: int
    page: str
    quantity: Union[int, str] = 1
    notes: str = ""
    use_quantity: bool = True
    content: str = ""
    link: str = ""

    def get_items(self, for_pdf=False):
        """Return the tuple of column values for this row."""
        if self.content:
            return (
                self.page,
                self.content,
                self.get_formatted_page(for_pdf),
            )
        if self.use_quantity:
            return (
                self.sheet,
                self.get_formatted_page(for_pdf),
                self.quantity,
                self.notes,
            )
        else:
            return (self.sheet, self.get_formatted_page(for_pdf), self.notes)

    def get_formatted_page(self, for_pdf):
        """Format the page column, hyperlinking HTML when not generating PDF."""
        target = str(self.link or self.page)
        if for_pdf:
            return target
        if target.endswith(".html"):
            href = target
        else:
            href = str(Path(target).with_suffix(".html"))
        return f"<a href={href}>{target}</a>"


@dataclass(frozen=True)
class IndexTable:
    rows: List[IndexTableRow]
    header: Tuple[str]

    @staticmethod
    def use_quantity_column(metadata: PagesMetadata):
        """Return True if quantity column should be shown (qty multipliers enabled)."""
        return metadata is not None and metadata.use_qty_multipliers

    @staticmethod
    def get_index_table_header(metadata: PagesMetadata = None, include_content=False):
        """Build the header tuple, optionally skipping quantity or adding content."""
        if include_content:
            return ("Name", "Content", "Page")
        skip = []
        if not IndexTable.use_quantity_column(metadata):
            skip.append("quantity")
        return (s.capitalize() for s in TABLE_COLUMNS if s not in skip)

    # TODO: how do we actually want to support this?
    @classmethod
    def from_pages_metadata(
        cls,
        metadata: PagesMetadata,
        options=None,
        paginated_pages: Dict[str, List[str]] = None,
    ):
        """Construct an index table from rendered pages metadata."""
        # detect split pages
        split_types = [
            ("bom", "BOM"),
            ("notes", "Notes"),
            ("index", "Index page"),
            ("cut", "Cut diagram"),
            ("termination", "Termination diagram"),
        ]
        has_split = False
        rows = []
        use_letters = (
            getattr(options, "table_page_suffix_letters", True) if options else True
        )

        # titlepage row
        rows.append(
            IndexTableRow(
                sheet=1,
                page=str(metadata.titlepage),
                notes="",
                use_quantity=False,
                content="Index page",
                link=str(Path(metadata.titlepage).with_suffix(".html")),
            )
        )

        # harness and split rows
        has_split = False
        for index, row in enumerate(metadata.output_names, start=2):
            base_link = str(Path(row).with_suffix(".html"))
            base_row = IndexTableRow(
                sheet=index,
                page=row,
                quantity=1,
                notes=metadata.pages_notes.get(row, ""),
                use_quantity=cls.use_quantity_column(metadata),
                content="Harness",
                link=base_link,
            )
            rows.append(base_row)
            for suffix, label in split_types:
                planned_suffixes = (
                    (paginated_pages or {}).get(suffix, None)
                    if paginated_pages is not None
                    else None
                )
                candidates: List[Union[Path, str]] = []
                if planned_suffixes:
                    candidates = [
                        f"{row}.{suffix}"
                        + (
                            f".{page_suffix or letter_suffix(idx)}"
                            if len(planned_suffixes) > 1
                            else ""
                        )
                        + ".html"
                        for idx, page_suffix in enumerate(planned_suffixes)
                    ]
                else:
                    candidates = sorted(
                        metadata.output_dir.glob(f"{row}.{suffix}*.html"),
                        key=lambda p: (
                            0 if p.stem == f"{row}.{suffix}" else 1,
                            p.stem,
                        ),
                    )
                if not candidates:
                    continue
                has_split = True
                total = len(candidates)
                for idx, candidate in enumerate(candidates):
                    suffix_letter = (
                        letter_suffix(idx) if use_letters and total > 1 else ""
                    )
                    page_name = f"{row}.{suffix}" + (
                        f".{suffix_letter}" if suffix_letter else ""
                    )
                    link = (
                        str(candidate)
                        if isinstance(candidate, str)
                        else str(candidate.relative_to(metadata.output_dir))
                    )
                    rows.append(
                        IndexTableRow(
                            sheet=index,
                            page=page_name,
                            notes="",
                            use_quantity=False,
                            content=label,
                            link=link,
                        )
                    )

        if not has_split:
            header = cls.get_index_table_header(metadata, include_content=False)
            qty_multipliers = None
            if cls.use_quantity_column(metadata):
                harnesses = HarnessQuantity(
                    metadata.files,
                    metadata.multiplier_file_name,
                    output_dir=metadata.output_dir,
                )
                harnesses.fetch_qty_multipliers_from_file()
                qty_multipliers = harnesses.multipliers

            rows = []
            for index, row in enumerate(metadata.output_names):
                if str(row) == "titlepage":
                    rows.append(
                        IndexTableRow(
                            sheet=1,
                            page=metadata.titlepage,
                            quantity="",
                            notes="",
                            use_quantity=cls.use_quantity_column(metadata),
                        )
                    )
                    continue
                quantity = qty_multipliers[row] if qty_multipliers is not None else 1
                rows.append(
                    IndexTableRow(
                        sheet=index + 1,
                        page=row,
                        quantity=quantity,
                        notes=metadata.pages_notes.get(row, ""),
                        use_quantity=cls.use_quantity_column(metadata),
                    )
                )
        else:
            header = cls.get_index_table_header(metadata, include_content=True)

        return cls(rows=rows, header=header)

    def render(self, options):
        return get_template("index_table.html").render(
            {
                "index_table": self,
                "options": options,
            }
        )
