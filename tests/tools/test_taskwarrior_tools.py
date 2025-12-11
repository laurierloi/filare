import importlib.util
import pathlib


def load_module(name: str, rel_path: str):
    """Load a module from scripts/ for testing."""
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    path = repo_root / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_ready_tasks_respects_dependencies_and_status(monkeypatch):
    mod = load_module("taskwarrior_next", "scripts/taskwarrior_next.py")
    Task = mod.Task

    t1 = Task(uid="U1", title="Task 1", role="FEATURE", status="PENDING", priority="M", depends=[], path="")
    t2 = Task(uid="U2", title="Task 2", role="FEATURE", status="PENDING", priority="M", depends=["U1"], path="")
    t3 = Task(uid="U3", title="Task 3", role="FEATURE", status="DONE", priority="M", depends=[], path="")

    ready_initial = mod.ready_tasks([t1, t2, t3], ["FEATURE"])
    assert [t.uid for t in ready_initial] == ["U1"]

    t1.status = "DONE"
    ready_after = mod.ready_tasks([t1, t2, t3], ["FEATURE"])
    assert [t.uid for t in ready_after] == ["U2"]


def test_next_branch_name_increments_on_collisions(monkeypatch):
    mod = load_module("taskwarrior_branch", "scripts/taskwarrior_branch.py")

    calls = {"count": 0}

    def fake_exists(name: str) -> bool:
        calls["count"] += 1
        return calls["count"] == 1  # first candidate exists, then free

    monkeypatch.setattr(mod, "branch_exists", fake_exists)

    branch = mod.next_branch_name("FEATURE", "Implement awesome feature")
    assert branch == "feature/implement-awesome-feature-2"


def test_split_pools_keeps_dependencies_together():
    mod = load_module("taskwarrior_split_pools", "scripts/taskwarrior_split_pools.py")
    entries = [
        {"uid": "A", "depends": []},
        {"uid": "B", "depends": ["A"]},
        {"uid": "C", "depends": []},
        {"uid": "D", "depends": ["C"]},
    ]
    comps = mod.build_components(entries)
    pools = mod.assign_pools(comps, 2)
    # Each dependency chain stays together
    assert any({"A", "B"} <= pool for pool in pools)
    assert any({"C", "D"} <= pool for pool in pools)
