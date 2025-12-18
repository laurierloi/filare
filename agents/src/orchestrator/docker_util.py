from __future__ import annotations

import subprocess
from typing import Dict, List, Optional


def docker_ps(label_filters: Dict[str, str]) -> List[str]:
    """Return container IDs matching the provided label filters."""
    args: List[str] = []
    for key, value in label_filters.items():
        args.extend(["--filter", f"label={key}={value}"])
    cmd = ["docker", "ps", "--quiet"] + args
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return [line for line in result.stdout.strip().splitlines() if line]


def docker_stop(container: str) -> None:
    subprocess.run(["docker", "stop", container], check=True)


def docker_logs(container: str, follow: bool) -> subprocess.Popen:
    args = ["docker", "logs"]
    if follow:
        args.append("-f")
    args.append(container)
    return subprocess.Popen(args)
