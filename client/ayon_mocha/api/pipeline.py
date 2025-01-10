"""Mocha Pro AYON pipeline API."""
from __future__ import annotations

import logging
import os
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import pyblish.api
from ayon_core.host import HostBase, ILoadHost, IPublishHost, IWorkfileHost
from ayon_core.pipeline import get_current_context
from ayon_core.tools.utils import host_tools
from mocha import ui

from .workio import current_file, file_extensions, open_file, save_file
from .lib import get_main_window

if TYPE_CHECKING:
    from qtpy import QtWidgets

log = logging.getLogger("ayon_mocha")
HOST_DIR = Path(__file__).resolve().parent
PLUGINS_DIR = HOST_DIR / "plugins"
PUBLISH_PATH = PLUGINS_DIR / "publish"
LOAD_PATH =  PLUGINS_DIR / "load"
CREATE_PATH = PLUGINS_DIR / "create"
INVENTORY_PATH = PLUGINS_DIR / "inventory"
STARTUP_PATH = PLUGINS_DIR / "startup"

AYON_CONTEXT_CREATOR_IDENTIFIER = "io.ayon.create.context"


class MochaProHost(HostBase, IWorkfileHost, ILoadHost, IPublishHost):
    """Mocha Pro host implementation."""

    name = "mochapro"

    def __init__(self):
        """Initialize the host."""
        super().__init__()

    def install(self) -> None:
        """Initialize the host."""
        pyblish.api.register_host(self.name)
        pyblish.api.register_plugin_path(PUBLISH_PATH.as_posix())

        #QtCore.QTimer.singleShot(0, self._install_menu)
        self._install_menu()

    def _install_menu(self) -> None:
        """Install the menu."""
        main_window = get_main_window()

        menu_label = os.getenv("AYON_MENU_LABEL", "AYON")
        menu = main_window.menuBar().addMenu(menu_label)

        action = menu.addAction("Current Context")

        def _on_menu_about_to_show(action: QtWidgets.QAction) -> None:
            """Update the menu."""
            context = get_current_context()
            action.setText(f"{context['folder_path']}, {context['task_name']}")

        action.setEnabled(False)
        menu.aboutToShow.connect(partial(_on_menu_about_to_show, action))
        menu.addSeparator()

        action = menu.addAction("Create...")
        action.triggered.connect(
            lambda: host_tools.show_publisher(
                parent=main_window, tab="create"))

        action = menu.addAction("Load...")
        action.triggered.connect(
            lambda: host_tools.show_loader(
                parent=main_window, use_context=True))

        action = menu.addAction("Publish...")
        action.triggered.connect(
            lambda: host_tools.show_publisher(
                parent=main_window, tab="publish"))

        action = menu.addAction("Manage...")
        action.triggered.connect(
            lambda: host_tools.show_scene_inventory(parent=main_window))

        action = menu.addAction("Library...")
        action.triggered.connect(
            lambda: host_tools.show_library_loader(parent=main_window))

        menu.addSeparator()

        action = menu.addAction("Work Files...")
        action.triggered.connect(
            lambda: host_tools.show_workfiles(parent=main_window))

        menu.addSeparator()

        action = menu.addAction("Experimental Tools...")
        action.triggered.connect(
            lambda: host_tools.show_experimental_tools_dialog(
                parent=main_window))

    def get_workfile_extensions(self) -> list[str]:
        """Get the workfile extensions."""
        return file_extensions()

    def save_workfile(self, dst_path: Optional[str]=None) -> None:
        """Save the workfile.

        Args:
            dst_path (str, optional): The destination path to save the file to.
                Defaults to None.


        Todo (antirotor): This needs to display error if the project
            isn't initialized yet.
            https://github.com/ynput/ayon-core/issues/1075

        """
        save_file(Path(dst_path) or None)

    def open_workfile(self, filepath: str) -> None:
        """Open the workfile."""
        open_file(Path(filepath))

    def get_current_workfile(self) -> Optional[str]:
        """Get the current workfile."""
        file_path = current_file()
        if file_path:
            return file_path.as_posix()
        return None

    def get_containers(self):
        pass

    def get_context_data(self) -> dict:
        """Get the context data."""
        return {}

    def update_context_data(self, data, changes):
        pass
