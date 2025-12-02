## Building docs locally (MkDocs)

The repo includes an `mkdocs.yml` that reuses the markdown files under `docs/`. To preview:

```bash
uv venv
uv sync --group dev
uv run --no-sync mkdocs serve -a 0.0.0.0:8000
```

To build static site into `site/`:

```bash
uv run --no-sync mkdocs build
```

## Sphinx API docs (optional)

Sphinx can be used to document the code (not wired yet). Suggested minimal setup:

```bash
uv add --group dev sphinx myst-parser sphinx-autodoc-typehints
uv run --no-sync sphinx-quickstart docs/api
```

Then add a simple `conf.py` pointing to `src/` and enable `autodoc` + `myst_parser` to mix Markdown with API docs.
