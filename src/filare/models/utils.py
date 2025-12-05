# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import List

awg_equiv_table = {
    "0.09": "28",
    "0.14": "26",
    "0.25": "24",
    "0.34": "22",
    "0.5": "21",
    "0.75": "20",
    "1": "18",
    "1.5": "16",
    "2.5": "14",
    "4": "12",
    "6": "10",
    "10": "8",
    "16": "6",
    "25": "4",
    "35": "2",
    "50": "1",
}

mm2_equiv_table = {v: k for k, v in awg_equiv_table.items()}


def awg_equiv(mm2):
    """Return the AWG gauge string for a given cross-sectional area in mm²."""
    return awg_equiv_table.get(str(mm2), "Unknown")


def mm2_equiv(awg):
    """Return the mm² cross-sectional area string for a given AWG gauge."""
    return mm2_equiv_table.get(str(awg), "Unknown")


def expand(yaml_data):
    """Expand range-like YAML entries (e.g., ``[1-3]``) into explicit lists.

    Args:
        yaml_data: Scalar or list that may include strings in ``a-b`` form.

    Returns:
        List with ranges expanded and individual entries coerced to int when possible.
    """
    # yaml_data can be:
    # - a singleton (normally str or int)
    # - a list of str or int
    # if str is of the format '#-#', it is treated as a range (inclusive) and expanded
    output = []
    if not isinstance(yaml_data, list):
        yaml_data = [yaml_data]
    for e in yaml_data:
        e = str(e)
        if "-" in e:
            a, b = e.split("-", 1)
            try:
                a = int(a)
                b = int(b)
                if a < b:
                    for x in range(a, b + 1):
                        output.append(x)  # ascending range
                elif a > b:
                    for x in range(a, b - 1, -1):
                        output.append(x)  # descending range
                else:  # a == b
                    output.append(a)  # range of length 1
            except:
                # '-' was not a delimiter between two ints, pass e through unchanged
                output.append(e)
        else:
            try:
                x = int(e)  # single int
            except Exception:
                x = e  # string
            output.append(x)
    return output


def get_single_key_and_value(d: dict):
    """Return the single key/value pair from a one-entry dict."""
    return next(iter(d.items()))


def int2tuple(inp):
    """Convert any value to a 1-tuple, preserving tuples."""
    if isinstance(inp, tuple):
        output = inp
    else:
        output = (inp,)
    return output


def flatten2d(inp):
    """Flatten a 2D list/tuple into a 2D list of strings."""
    return [
        [str(item) if not isinstance(item, List) else ", ".join(item) for item in row]
        for row in inp
    ]


# TODO: move to hyperlink
def html_line_breaks(inp):
    """Convert newlines to HTML <br /> tags after stripping links."""
    return remove_links(inp).replace("\n", "<br />") if isinstance(inp, str) else inp


# TODO: move to hyperlink
def remove_links(inp):
    """Strip HTML anchor tags, returning just the link text."""
    return (
        re.sub(r"<[aA] [^>]*>([^<]*)</[aA]>", r"\1", inp)
        if isinstance(inp, str)
        else inp
    )


def clean_whitespace(inp):
    """Collapse repeated whitespace and tidy stray spaces before punctuation."""
    return " ".join(inp.split()).replace(" ,", ",") if isinstance(inp, str) else inp


def smart_file_resolve(filename: Path, possible_paths: (Path, List[Path])) -> Path:
    if isinstance(possible_paths, Path) or isinstance(possible_paths, str):
        possible_paths = [possible_paths]
    if filename.is_absolute():
        if filename.exists():
            return filename
        else:
            raise Exception(f"{filename} does not exist.")
    else:  # search all possible paths in decreasing order of precedence
        for path in possible_paths:
            combined_path = (path / filename).resolve()
            if combined_path.exists():
                return combined_path
        raise Exception(
            f"{filename} was not found in any of the following locations: \n"
            + "\n".join(str(p) for p in possible_paths)
        )
