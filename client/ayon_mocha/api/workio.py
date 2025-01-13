"""Host API for working with workfiles."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from mocha.project import Clip, Project, get_current_project


def file_extensions() -> list[str]:
    """Return file extensions for workfiles."""
    return [".mocha"]

def has_unsave_changes() -> bool:
    """Return True if the current workfile has unsaved changes.

    Mocha Pro doesn't have API to query this state so we always return False.
    """
    return True

def save_file(filepath:Optional[Path]) -> None:
    """Save the current workfile.

    Note that project cannot be saved without being created first.
    To create the project, you need to specify clip first, thus
    we can't create workfile from the un-initialized project within Mocha Pro.

    """
    project = get_current_project()
    if not project:
        project = _create_empy_project()
    if filepath:
        project.save_as(filepath.as_posix())
        return
    project.save()

def open_file(filepath:Optional[Path]) -> None:
    """Open a workfile."""
    Project(filepath.as_posix())

def current_file() -> Optional[Path]:
    """Return the current workfile."""
    project = get_current_project()
    if not project:
        return None
    return Path(project.project_file)

def _create_empy_project() -> Project:
    """Create an empty project."""
    clip = Clip("/foo/bar")
    return Project(clip)
