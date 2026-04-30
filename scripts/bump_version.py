#!/usr/bin/env python3
"""Bump the patch version in pyproject.toml and [project]/__init__.py when needed.

Usage:
    python scripts/bump_version.py <pyproject-path>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


VERSION_RE = re.compile(r'^(\s*version\s*=\s*")(?P<version>[0-9]+(?:\.[0-9]+)*)("\s*)$')
NAME_RE = re.compile(r'^\s*name\s*=\s*"(?P<name>[^"]+)"\s*$')
INIT_VERSION_RE = re.compile(r"^(\s*version\s*=\s*')(?P<version>[0-9]+(?:\.[0-9]+)*)('\s*)$")


def bump_patch(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def main() -> int:
    # Always auto-discover pyproject.toml by searching upwards from script location
    current = Path(__file__).resolve().parent
    root = current.anchor
    pyproject_path = None
    while True:
        candidate = current / "pyproject.toml"
        if candidate.exists():
            pyproject_path = candidate
            break
        if str(current) == root:
            break
        current = current.parent
    if not pyproject_path:
        print("pyproject.toml not found.", file=sys.stderr)
        return 2

    text = pyproject_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    package_name: str | None = None
    for line in lines:
        name_match = NAME_RE.match(line)
        if name_match:
            package_name = name_match.group("name").replace("-", "_")
            break

    for index, line in enumerate(lines):
        match = VERSION_RE.match(line)
        if not match:
            continue

        current_version = match.group("version")
        new_version = bump_patch(current_version)
        lines[index] = f'{match.group(1)}{new_version}{match.group(3)}'
        pyproject_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        init_path = pyproject_path.parent / package_name / "__init__.py" if package_name else None
        if init_path and init_path.exists():
            init_lines = init_path.read_text(encoding="utf-8").splitlines()
            for i, init_line in enumerate(init_lines):
                init_match = INIT_VERSION_RE.match(init_line)
                if init_match:
                    init_lines[i] = f"{init_match.group(1)}{new_version}{init_match.group(3)}"
                    break
            init_path.write_text("\n".join(init_lines) + "\n", encoding="utf-8")

        print(new_version)
        return 0

    print("No [project].version entry found in pyproject.toml", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
