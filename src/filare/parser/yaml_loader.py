"""Parse yaml files while supporting updates (newer files modify previous definitions)"""

from functools import reduce
from pathlib import Path
from typing import Any, Dict, List

import yaml


def merge_item(x, y):
    """Merge two YAML-derived values with list concatenation and dict recursion."""
    if y is None:
        ret = x
    elif x is None:
        ret = y
    else:
        if type(x) != type(y):
            ret = y
        elif isinstance(x, dict):
            keys = set(x.keys()).union(set(y.keys()))
            new_dict = {}
            for k in keys:
                if k in x and k in y:
                    new_dict[k] = merge_item(x[k], y[k])
                elif k in x:
                    new_dict[k] = x[k]
                elif k in y:
                    new_dict[k] = y[k]
                else:
                    raise RuntimeError(
                        f"Key {k} not in x or y, this should never happen!"
                    )
            ret = new_dict
        elif isinstance(x, list):
            ret = x + y
        else:  # y dominates
            ret = y
    return ret


def merge_content(content: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Reduce a list of YAML fragments into a single merged dict."""
    return reduce(merge_item, content)


def parse_merge_yaml(_yamls: List[str]) -> Dict[str, Any]:
    """Parse and merge multiple YAML strings, applying merge semantics."""
    if not _yamls:
        return {}
    loaded = safe_load_yaml(_yamls)
    return merge_content(loaded)


def safe_load_yaml(texts: List[str]) -> List[Dict[str, Any]]:
    """Load YAML strings while preserving ints as strings to avoid mangling."""
    loader = yaml.loader.SafeLoader
    loader.construct_yaml_int = loader.construct_yaml_str
    # Keep all int as string, because component number tend to be int and can be mangled by the cast
    loader.yaml_constructors["tag:yaml.org,2002:int"] = loader.yaml_constructors[
        "tag:yaml.org,2002:str"
    ]
    return [yaml.load(_yaml, Loader=loader) for _yaml in texts]


def parse_merge_files(files: List[Path]) -> Dict[str, Any]:
    """Load multiple YAML files and merge their content."""
    content = []
    return parse_merge_yaml([f.open("r").read() for f in files])


def parse_concat_merge_files(concats: List[Path], merge: List[Path]) -> Dict[str, Any]:
    """Concatenate a list of YAML files, then merge with another list."""
    return parse_merge_yaml(
        [
            "\n".join([f.open("r").read() for f in concats]),
            *[f.open("r").read() for f in merge],
        ]
    )
