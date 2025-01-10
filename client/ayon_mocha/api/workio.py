"""Host API for working with workfiles."""
from __future__ import annotations

from pathlib import Path
from shutil import copyfile
from typing import Optional

from mocha.project import Clip, Project, get_current_project

from ayon_mocha import MOCHA_ADDON_ROOT

from .lib import update_ui


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
        project = _create_empy_project(filepath)
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

def _create_empy_project(path: Path) -> Project:
    """Create an empty project."""
    clip_path = _copy_placeholder_clip(path.parent)
    clip = Clip(clip_path.as_posix())
    project = Project(clip)

    update_ui()
    return project

def _copy_placeholder_clip(destination:Path) -> Path:
    """Copy placeholder clip to the destination."""
    clip_path = destination / "empty.exr"
    copyfile(
        Path(MOCHA_ADDON_ROOT) / "resources" / "empty.exr",
        clip_path
    )
    return clip_path
