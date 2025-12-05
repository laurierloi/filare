# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from weasyprint import HTML


def generate_pdf_output(
    filename_list: List[Path],
):
    """Render a list of HTML files into a single PDF.

    Args:
        filename_list: List of harness HTML paths (or a single path). When multiple
            files are provided, the PDF is named after the containing directory.

    Returns:
        None. Writes a PDF next to the input files.

    Raises:
        FileNotFoundError: If an input HTML file is missing.
        Exception: If WeasyPrint fails to render or write the PDF.
    """
    if isinstance(filename_list, Path):
        filename_list = [filename_list]
        output_path = filename_list[0].with_suffix(".pdf")
    else:
        output_dir = filename_list[0].parent
        output_path = (output_dir / output_dir.name).with_suffix(".pdf")

    filepath_list = [f.with_suffix(".html") for f in filename_list]

    print(f"Generating pdf output: {output_path}")
    files_html = [HTML(path) for path in filepath_list]
    documents = [f.render() for f in files_html]
    all_pages = [p for doc in documents for p in doc.pages]
    documents[0].copy(all_pages).write_pdf(output_path)
