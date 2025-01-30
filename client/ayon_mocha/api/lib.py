"""Library functions for the Ayon Mocha API."""
from __future__ import annotations

import dataclasses
import re
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path
from shutil import copyfile
from typing import TYPE_CHECKING, Any, Optional

from mocha import get_mocha_exec_name, ui
from mocha.exporters import TrackingDataExporter
from mocha.project import Clip, Project
from qtpy.QtWidgets import QApplication

from ayon_mocha.addon import MOCHA_ADDON_ROOT

if TYPE_CHECKING:
    from qtpy import QtWidgets


EXTENSION_PATTERN = re.compile(r"(?P<name>.+)\(\*\.(?P<ext>\w+)\)")


"""
These dataclasses are here because they
cannot be defined directly in pyblish plugins.
There seems to be an issue (at least in python 3.7)
with dataclass checking for __module__ in class and
that one is missing in discovered pyblish
plugin classes.
"""
@dataclasses.dataclass
class ExporterInfo:
    """Exporter information."""
    id: str
    label: str
    exporter: TrackingDataExporter


@dataclasses.dataclass
class ExporterProcessInfo:
    """Exporter process information."""
    mocha_python_path: Path
    mocha_exporter_path: Path
    current_project_path: Path
    staging_dir: Path
    options: dict[str, bool]


def get_main_window() -> QtWidgets.QWidget:
    """Get the main window of the application.

    Returns:
        QWidget: Main window of the application.
    """
    return ui.get_widgets()["MainWindow"]

def update_ui() -> None:
    """Update the UI."""
    QApplication.processEvents()


def run_mocha(
        app: str="mochapro",
        footage_path: str="",
        **kwargs: dict[str, Any]) -> None:
    """Run Mocha application with given command-line arguments.

    See https://borisfx.com/support/documentation/mocha/#_command_line

    This is modified version of the original function from mocha module.
    We need to pass the environment to the subprocess.Popen call.

    Todo:
        - return something so we quit the parent app only if the new
            app is running
        - refactor this function to use the subprocess.run function

    Args:
        app (str): Application name (without an extension).
        footage_path (str): An absolute path to footage file.
        **kwargs: Keyword arguments for command line.

    Keywords mapping::

        in_point => --in
        out_point => --out
        frame_rate => --frame-rate
        par => --par
        interlace_mode => --interlace-mode
    """
    import os
    mocha_path = get_mocha_exec_name(app)
    if not os.path.isfile(mocha_path):
        return

    available_args = {
        "in_point": "in",
        "out_point": "out",
        "frame_rate": "frame-rate",
        "par": "par",
        "interlace_mode": "interlace-mode"
    }
    available_keys = set(available_args.keys())
    current_keys = set(kwargs.keys())
    if not current_keys <= available_keys:
        msg = (
            "No such parameters: "
            ", ".join(current_keys - available_keys)
        )
        raise ValueError(msg)


    cmd_args: list[str] = []
    for key, value in kwargs.items():
        cmd_args.extend((f"--{available_args[key]}", str(value)))
    cmd = [mocha_path, *cmd_args]
    if footage_path:
        cmd.append(footage_path)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    if os.name == "nt":
        p = subprocess.Popen(
            cmd, creationflags=0x00000008, close_fds=True, env=env)
    else:
        p = subprocess.Popen(
            cmd, close_fds=True, env=env)
    p.poll()


def quit_mocha() -> None:
    """Quit Mocha application."""
    # this code unfortunately doesn't work
    # menu_file = ui.get_menus()["MenuFile"]
    # quit_action = next(
    #   filter(lambda a: a.objectName() == "FileExit", menu_file.actions()))
    # quit_action.triggered.emit()
    # so we need to use this workaround
    QApplication.instance().quit()


def copy_placeholder_clip(destination:Path) -> Path:
    """Copy placeholder clip to the destination."""
    clip_path = destination / "empty.exr"
    copyfile(
        Path(MOCHA_ADDON_ROOT) / "resources" / "empty.exr",
        clip_path
    )
    return clip_path


def create_empy_project(
        project_path: Optional[Path] = None) -> Project:
    """Create an empty project."""
    if not project_path:
        project_path = Path(tempfile.NamedTemporaryFile(
            suffix=".mocha", delete=False).name)

    clip_path = copy_placeholder_clip(project_path.parent)
    clip = Clip(clip_path.as_posix())
    return Project(clip)


def get_exporters() -> list[ExporterInfo]:
    """Return all registered exporters as a list."""
    return [
        ExporterInfo(
            id=sha256(k.encode()).hexdigest(),
            label=k,
            exporter=v)
        for k, v in sorted(
            TrackingDataExporter.registered_exporters().items())
    ]
