#!/usr/bin/env python3
"""Bump the patch version in pyproject.toml when needed.

Usage:
    python scripts/bump_pyproject_version.py <pyproject-path>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


VERSION_RE = re.compile(r'^(\s*version\s*=\s*")(?P<version>[0-9]+(?:\.[0-9]+)*)("\s*)$')


def bump_patch(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: bump_pyproject_version.py <pyproject-path>", file=sys.stderr)
        return 2

    pyproject_path = Path(sys.argv[1])
    text = pyproject_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for index, line in enumerate(lines):
        match = VERSION_RE.match(line)
        if not match:
            continue

        current_version = match.group("version")
        new_version = bump_patch(current_version)
        lines[index] = f'{match.group(1)}{new_version}{match.group(3)}'
        pyproject_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(new_version)
        return 0

    print("No [project].version entry found in pyproject.toml", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
