"""Host API for working with workfiles."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from mocha.project import get_current_project

from .lib import create_empty_project, quit_mocha, run_mocha


def file_extensions() -> list[str]:
    """Return file extensions for workfiles."""
    return [".mocha"]


def has_unsave_changes() -> bool:
    """Return True if the current workfile has unsaved changes.

    Mocha Pro doesn't have API to query this state so we always return False.
    """
    return True


def save_file(filepath: Optional[Path]) -> None:
    """Save the current workfile.

    Note that project cannot be saved without being created first.
    To create the project, you need to specify clip first, thus
    we can't create workfile from the un-initialized project within Mocha Pro.

    """
    project = get_current_project()
    if not project:
        if not filepath:
            return
        project = create_empty_project(filepath)
    if filepath:
        project.save_as(filepath.as_posix())
        # now we need to reopen mocha with the new project
        open_file(filepath)
        return
    project.save()


def open_file(filepath: Path) -> None:
    """Open a workfile.

    There is probably no way to open a workfile in Mocha Pro directly,
    so we run Mocha Pro with the footage file as an argument, this will
    open new Mocha Pro window with the project loaded, and we kill the
    original application.There wasn't even a way to quit Mocha Pro
    in standard way, so we terminate it rather forcefully.

    Todo (antirotor): quit mocha only if the run_mocha was successful.

    Args:
        filepath (Path): Path to the workfile.

    """
    run_mocha(footage_path=filepath.as_posix())
    quit_mocha()


def current_file() -> Optional[Path]:
    """Return the current workfile."""
    project = get_current_project()
    if not project:
        return None
    return Path(project.project_file)
