import sys
from pathlib import Path


def pytest_configure(config):
    repo_root = Path(__file__).resolve().parents[2]
    orchestrator_src = repo_root / "agents" / "src"
    if orchestrator_src.exists():
        sys.path.insert(0, str(orchestrator_src))
