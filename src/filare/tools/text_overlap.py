"""
Tooling CLI to detect overlapping text in rendered HTML using Playwright.

Usage:
  uv run filare-check-overlap outputs/**/*.html --viewport 1280x720
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

import yaml
from playwright.sync_api import Page, sync_playwright

from filare.errors import FilareToolsException, ViewportParseError


DEFAULT_VIEWPORT = (1280, 720)
DEFAULT_WARN_THRESHOLD = 1.0
DEFAULT_ERROR_THRESHOLD = 2.0
DEFAULT_IGNORE_CONFIG = ".filare-overlap-ignore.yml"


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


@dataclass
class Node:
    text: str
    rect: Rect
    tag: str
    id_attr: str
    classes: List[str]


@dataclass
class Overlap:
    depth: float
    severity: str
    a: Node
    b: Node


@dataclass
class IgnoreRules:
    selectors: List[str]
    text_patterns: List[re.Pattern]


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect overlapping text in rendered HTML."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="HTML files or glob patterns to check (default: include all matches).",
    )
    parser.add_argument(
        "--viewport",
        default=f"{DEFAULT_VIEWPORT[0]}x{DEFAULT_VIEWPORT[1]}",
        help="Viewport size WIDTHxHEIGHT (default: 1280x720).",
    )
    parser.add_argument(
        "--warn-threshold",
        type=float,
        default=DEFAULT_WARN_THRESHOLD,
        help="Warn when overlap depth exceeds this value in px (default: 1.0).",
    )
    parser.add_argument(
        "--error-threshold",
        type=float,
        default=DEFAULT_ERROR_THRESHOLD,
        help="Error when overlap depth exceeds this value in px (default: 2.0).",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Write JSON report to this path.",
    )
    parser.add_argument(
        "--ignore-selector",
        action="append",
        default=[],
        help="CSS selector to ignore (can be repeated).",
    )
    parser.add_argument(
        "--ignore-text",
        action="append",
        default=[],
        help="Regex for text to ignore (can be repeated).",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_IGNORE_CONFIG,
        help="Path to overlap ignore config (YAML). Default: .filare-overlap-ignore.yml",
    )
    return parser.parse_args(argv)


def parse_viewport(value: str) -> tuple[int, int]:
    if "x" not in value:
        raise ViewportParseError(value)
    w_str, h_str = value.lower().split("x", 1)
    return int(w_str), int(h_str)


def load_ignore_config(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def compile_ignores(
    config: dict, extra_selectors: List[str], extra_text: List[str], page_path: Path
) -> IgnoreRules:
    selectors = list(config.get("selectors", [])) + extra_selectors
    text_patterns = [
        re.compile(p) for p in config.get("text_patterns", []) + extra_text
    ]

    pages = config.get("pages", {}) or {}
    page_str = str(page_path)
    for pattern, page_rules in pages.items():
        if fnmatch.fnmatch(page_str, pattern):
            selectors.extend(page_rules.get("selectors", []))
            text_patterns.extend(
                re.compile(p) for p in page_rules.get("text_patterns", [])
            )

    return IgnoreRules(selectors=selectors, text_patterns=text_patterns)


def discover_files(patterns: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        paths = (
            list(Path().glob(pattern))
            if any(ch in pattern for ch in "*?[]")
            else [Path(pattern)]
        )
        for path in paths:
            if path.is_file() and path.suffix.lower() == ".html":
                files.append(path)
    return sorted({p.resolve() for p in files})


def gather_nodes(page: Page, ignore_selectors: List[str]) -> List[Node]:
    script = """
    (selectors) => {
      const ignored = selectors || [];
      const results = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        const text = (node.textContent || "").trim();
        if (!text) continue;
        const el = node.parentElement;
        if (!el) continue;
        if (ignored.length && ignored.some(sel => {
          try { return el.matches(sel); } catch { return false; }
        })) {
          continue;
        }
        const style = getComputedStyle(el);
        if (style.display === "none" || style.visibility === "hidden" || parseFloat(style.opacity || "1") === 0) {
          continue;
        }
        const range = document.createRange();
        range.selectNodeContents(node);
        const rect = range.getBoundingClientRect();
        if (!rect || rect.width === 0 || rect.height === 0) {
          continue;
        }
        results.push({
          text: text.substring(0, 120),
          rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
          tag: el.tagName,
          id_attr: el.id || "",
          classes: Array.from(el.classList || []),
        });
      }
      return results;
    }
    """
    raw_nodes = page.evaluate(script, ignore_selectors)
    return [
        Node(
            text=item["text"],
            rect=Rect(
                x=float(item["rect"]["x"]),
                y=float(item["rect"]["y"]),
                width=float(item["rect"]["width"]),
                height=float(item["rect"]["height"]),
            ),
            tag=item["tag"],
            id_attr=item["id_attr"],
            classes=item["classes"],
        )
        for item in raw_nodes
    ]


def filter_nodes_by_text(
    nodes: List[Node], text_patterns: List[re.Pattern]
) -> List[Node]:
    if not text_patterns:
        return nodes
    filtered = []
    for node in nodes:
        if any(pattern.search(node.text) for pattern in text_patterns):
            continue
        filtered.append(node)
    return filtered


def compute_overlaps(
    nodes: List[Node], warn_threshold: float, error_threshold: float
) -> List[Overlap]:
    overlaps: List[Overlap] = []
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            dx = min(a.rect.right, b.rect.right) - max(a.rect.x, b.rect.x)
            dy = min(a.rect.bottom, b.rect.bottom) - max(a.rect.y, b.rect.y)
            if dx <= 0 or dy <= 0:
                continue
            depth = min(dx, dy)
            severity: Optional[str] = None
            if depth > error_threshold:
                severity = "error"
            elif depth > warn_threshold:
                severity = "warning"
            if severity:
                overlaps.append(Overlap(depth=depth, severity=severity, a=a, b=b))
    return overlaps


def node_hint(node: Node) -> str:
    ident_parts = [node.tag.lower()]
    if node.id_attr:
        ident_parts.append(f"#{node.id_attr}")
    if node.classes:
        ident_parts.append("." + ".".join(node.classes))
    return "".join(ident_parts)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        viewport = parse_viewport(args.viewport)
    except FilareToolsException as exc:
        print(f"Invalid viewport: {exc}", file=sys.stderr)
        return 2

    html_files = discover_files(args.paths)
    if not html_files:
        print("No HTML files found for provided paths.", file=sys.stderr)
        return 2

    config = load_ignore_config(Path(args.config))

    report = {"files": []}
    any_errors = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]}
        )
        for file_path in html_files:
            page = context.new_page()
            url = file_path.resolve().as_uri()
            page.goto(url)
            rules = compile_ignores(
                config, args.ignore_selector, args.ignore_text, file_path
            )
            nodes = gather_nodes(page, rules.selectors)
            nodes = filter_nodes_by_text(nodes, rules.text_patterns)
            overlaps = compute_overlaps(
                nodes, args.warn_threshold, args.error_threshold
            )
            errors = [o for o in overlaps if o.severity == "error"]
            any_errors = any_errors or bool(errors)
            file_entry = {
                "file": str(file_path),
                "overlaps": [
                    {
                        "severity": o.severity,
                        "depth": o.depth,
                        "a": {
                            "text": o.a.text,
                            "selector": node_hint(o.a),
                            "rect": o.a.rect.__dict__,
                        },
                        "b": {
                            "text": o.b.text,
                            "selector": node_hint(o.b),
                            "rect": o.b.rect.__dict__,
                        },
                    }
                    for o in overlaps
                ],
            }
            report["files"].append(file_entry)
        browser.close()

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")

    total_warn = sum(
        len([o for o in f["overlaps"] if o["severity"] == "warning"])
        for f in report["files"]
    )
    total_err = sum(
        len([o for o in f["overlaps"] if o["severity"] == "error"])
        for f in report["files"]
    )
    print(
        f"Checked {len(html_files)} HTML file(s); warnings: {total_warn}, errors: {total_err}"
    )
    if total_warn:
        print("Warnings detected (overlaps above warn threshold).")
    if total_err:
        print("Errors detected (overlaps above error threshold).", file=sys.stderr)
    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main())
