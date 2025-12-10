# Functional examples test is skipped due to OOM risk

## Category

TEST

## Evidence

- `tests/documentation/test_examples_and_tutorial.py::test_examples_generate_outputs` is marked `@pytest.mark.skip(reason="This tests just gets the system OOM... there's some leak somewhere")`.
- The test invokes `run_filare_cli(...)` to render all `examples/ex*.yml` (HTML) using the Typer callback `render_callback`, not a subprocess.
- `just test-functional` reports this test as skipped.

## Hypothesis

- Since the CLI moved from Click to Typer and the test now calls the Typer callback in-process, each example render keeps harness/Graphviz objects alive (e.g., `Harness._graph`, cached BOM/index tables). Rendering all examples in one process may accumulate large objects, triggering OOM.
- Running each example via the actual CLI binary (separate processes) likely avoided this in the past; the in-process Typer call makes any leak or missing cleanup visible.

## Suggested Next Steps

- Add explicit teardown/cleanup in `run_filare_cli` (e.g., drop `harness._graph`, close file handles) or run examples in subprocesses to isolate memory use.
- Profile memory during a reduced set of examples to confirm retention (look for lingering `Harness`/Graphviz objects).
- Unskip the test after tightening memory/cleanup and ensuring it completes on CI with Typer.

## Steps Taken

- Adjusted `run_filare_cli` to render each example in its own `uv run filare run ...` subprocess, reusing the sanitized inputs but isolating memory between runs.
- Re-ran `tests/documentation/test_examples_and_tutorial.py::test_examples_generate_outputs` with a 1 GB virtual memory limit (`ulimit -v 1048576`) and functional tests enabled; it now passes with ~105 MB max RSS.
- Unskipped the test.

## Status

- Resolved.
