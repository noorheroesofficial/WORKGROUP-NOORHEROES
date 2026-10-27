"""
NoorHeroes Cross-Platform Workgroup Root & Path Resolution Utility
==================================================================
Provides dynamic, zero-hardcoding discovery of the WORKGROUP-NOORHEROES
repository root across Windows, Linux, and macOS.

Supports:
- Execution from any child directory or submodule
- Moving or copying the workgroup to any laptop, drive, or user directory
- WORKGROUP_ROOT environment variable override
- Canonical POSIX relative path calculation
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

_ROOT_MARKER = ".workgroup-root"
_FALLBACK_MARKERS = ("PROJECT-CONTEXT.md", "DEVELOPMENT-RULES.md")
_CACHED_ROOT: Optional[Path] = None


def get_workgroup_root(start_path: Optional[Path | str] = None) -> Path:
    """
    Dynamically discovers the absolute Path of the WORKGROUP-NOORHEROES root.

    Algorithm:
    1. Check for WORKGROUP_ROOT environment variable override.
    2. Ascend from start_path (or __file__ if not provided) looking for .workgroup-root.
    3. If not found, ascend from current working directory (Path.cwd()).
    4. Validate and cache the discovered root.
    """
    global _CACHED_ROOT

    # 1. Environment Variable Override (if valid)
    env_root = os.environ.get("WORKGROUP_ROOT")
    if env_root:
        candidate = Path(env_root).resolve()
        if candidate.is_dir() and (candidate / _ROOT_MARKER).exists():
            _CACHED_ROOT = candidate
            return candidate

    if _CACHED_ROOT is not None and start_path is None:
        return _CACHED_ROOT

    # 2. Ascend from starting path or file location
    current = Path(start_path).resolve() if start_path else Path(__file__).resolve().parent
    for candidate in [current, *current.parents]:
        if (candidate / _ROOT_MARKER).exists():
            _CACHED_ROOT = candidate
            return candidate
        if all((candidate / m).exists() for m in _FALLBACK_MARKERS):
            _CACHED_ROOT = candidate
            return candidate

    # 3. Ascend from current working directory
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / _ROOT_MARKER).exists():
            _CACHED_ROOT = candidate
            return candidate
        if all((candidate / m).exists() for m in _FALLBACK_MARKERS):
            _CACHED_ROOT = candidate
            return candidate

    raise FileNotFoundError(
        "Could not determine WORKGROUP root. Ensure '.workgroup-root' exists at the workgroup "
        "root or set the WORKGROUP_ROOT environment variable."
    )


def resolve_workgroup_path(*parts: str | Path) -> Path:
    """
    Resolves a path relative to the dynamically discovered WORKGROUP root.
    Handles cross-platform separators automatically via pathlib.
    """
    root = get_workgroup_root()
    if not parts:
        return root
    return (root.joinpath(*parts)).resolve()


def get_relative_workgroup_path(path: str | Path) -> str:
    """
    Returns the POSIX-compliant relative path of any target file/directory
    relative to the WORKGROUP root.
    """
    target = Path(path).resolve()
    root = get_workgroup_root()
    return target.relative_to(root).as_posix()


# Subsystem Path Accessors
def get_backend_dir() -> Path:
    return resolve_workgroup_path("NoorHeroes-Backend")


def get_admin_dir() -> Path:
    return resolve_workgroup_path("noorheroes-admin")


def get_mobile_dir() -> Path:
    return resolve_workgroup_path("NoorHeroes")


def get_prds_dir() -> Path:
    return resolve_workgroup_path("PRD_Documents")


def get_blueprints_dir() -> Path:
    return resolve_workgroup_path("Development_Blueprints")


def get_screens_dir() -> Path:
    return resolve_workgroup_path("Screens")


def get_changelog_dir() -> Path:
    return resolve_workgroup_path("CHANGELOG")


if __name__ == "__main__":
    try:
        root = get_workgroup_root()
        if len(sys.argv) > 1:
            target = resolve_workgroup_path(*sys.argv[1:])
            print(str(target))
        else:
            print(str(root))
    except Exception as err:
        sys.stderr.write(f"Error: {err}\n")
        sys.exit(1)
