"""Mocha Pro AYON pipeline API."""
from __future__ import annotations

import dataclasses
import json
import logging
import os
import re
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Generator, Optional, Union

import pyblish.api
from ayon_core.host import (
    HostBase,
    ILoadHost,
    IPublishHost,
    IWorkfileHost,
)
from ayon_core.pipeline import (
    AYON_CONTAINER_ID,
    CreatedInstance,
    get_current_context,
)
from ayon_core.tools.utils import host_tools
from mocha.project import get_current_project

from .lib import get_main_window
from .workio import current_file, file_extensions, open_file, save_file

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

AYON_CONTEXT_CREATOR_ID = "io.ayon.create.context"
AYON_METADATA_GUARD = "AYON_CONTEXT::{}::AYON_CONTEXT_END"
AYON_METADATA_REGEX = re.compile(
    AYON_METADATA_GUARD.format("(?P<context>.*?)"),
    re.DOTALL)

MOCHA_CONTEXT_KEY = "context"
MOCHA_INSTANCES_KEY = "publish_instances"
MOCHA_CONTAINERS_KEY = "containers"

class AYONJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for dataclasses."""

    def default(self, obj: object) -> Union[dict, object]:
        """Encode dataclasses as dict."""
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj) # type: ignore[arg-type]
        if isinstance(obj, CreatedInstance):
            return dict(obj)
        return super().default(obj)

@dataclasses.dataclass
class Container:
    """Container data class."""

    name: Optional[str] = None
    id: str = AYON_CONTAINER_ID
    namespace: str = ""
    loader: Optional[str] = None
    representation: Optional[str] = None
    objectName: Optional[str] = None  # noqa: N815
    timestamp: int = 0
    version: Optional[str] = None


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

        def _on_menu_about_to_show(menu_action: QtWidgets.QAction) -> None:
            """Update the menu."""
            context = get_current_context()
            menu_action.setText(
                f"{context['folder_path']}, {context['task_name']}")

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
        if dst_path:
            save_file(Path(dst_path))
        else:
            save_file(filepath=None)

    def open_workfile(self, filepath: str) -> None:
        """Open the workfile."""
        open_file(Path(filepath))

    def get_current_workfile(self) -> Optional[str]:
        """Get the current workfile."""
        file_path = current_file()
        return file_path.as_posix() if file_path else None

    def get_containers(self) -> Generator[Container, None, list]:
        """Get containers from the current workfile."""
        # sourcery skip: use-named-expression
        data = self.get_ayon_data()
        if data:
            yield from data.get(MOCHA_CONTAINERS_KEY, [])
        return []

    def add_container(self, container: Container) -> None:
        """Add a container to the current workfile.

        Args:
            container (Container): Container to add.

        """
        data = self.get_ayon_data()
        containers = list(self.get_containers())
        to_remove = [
            idx
            for idx, _container in enumerate(containers)
            if _container.name == container.name
            and _container.namespace == container.namespace
        ]
        for idx in reversed(to_remove):
            containers.pop(idx)

        data[MOCHA_CONTAINERS_KEY] = [
            *containers, dataclasses.asdict(container)]

        self.update_ayon_data(data)

    def _create_ayon_data(self) -> None:
        """Create AYON data in the current project."""
        project = get_current_project()
        project.notes = (
            f"{project.notes}\n"
            f"{AYON_METADATA_GUARD}\n")

    def get_ayon_data(self) -> dict:
        """Get AYON context data from the current project.

        Mocha Pro doesn't have any custom node or other
        place to store metadata, so we store context data in
        the project notes encoded as JSON and wrapped in a
        special guard string `AYON_CONTEXT::...::AYON_CONTEXT_END`.

        Returns:
            dict: Context data.

        """
        # sourcery skip: use-named-expression
        project = get_current_project()
        m = re.search(AYON_METADATA_REGEX, project.notes)
        if not m:
            self._create_ayon_data()
            return {}
        try:
            context = json.loads(m["context"]) if m else {}
        except ValueError:
            self.log.debug("AYON data is not valid json")
            # AYON data not found or invalid, create empty placeholder
            self._create_ayon_data()
            return {}

        return context

    def update_ayon_data(self, data: dict) -> None:
        """Update AYON context data in the current project.

        Serialize context data as json and store it in the
        project notes. If the context data is not found, create
        a placeholder there. See `get_context_data` for more info.

        Args:
            data (dict): Context data.

        """
        project = get_current_project()
        original_data = self.get_ayon_data()

        updated_data = original_data.copy()
        updated_data.update(data)
        update_str = json.dumps(
            updated_data or {}, indent=4, cls=AYONJSONEncoder)

        project.notes = re.sub(
                AYON_METADATA_REGEX,
                AYON_METADATA_GUARD.format(update_str),
                project.notes,
            )

    def get_context_data(self) -> dict:
        """Get context data from the current project."""
        data = self.get_ayon_data()

        return data.get(MOCHA_CONTEXT_KEY, {})

    def update_context_data(self, data: dict, changes: dict) -> None:
        """Update context data in the current project.

        Args:
            data (dict): Context data.
            changes (dict): Changes to the context data.

        Raises:
            RuntimeError: If the context data is not found.

        """
        if not data:
            return
        ayon_data = self.get_ayon_data()
        ayon_data[MOCHA_CONTEXT_KEY] = data
        self.update_ayon_data(ayon_data)


    def get_publish_instances(self) -> list[dict]:
        """Get publish instances from the current project."""
        data = self.get_ayon_data()
        return data.get(MOCHA_INSTANCES_KEY, [])

    def add_publish_instance(self, instance_data: dict) -> None:
        """Add a publish instance to the current project.

        Args:
            instance_data (dict): Publish instance to add.

        """
        data = self.get_ayon_data()
        publish_instances = self.get_publish_instances()
        publish_instances.append(instance_data)
        data[MOCHA_INSTANCES_KEY] = publish_instances

        self.update_ayon_data(data)

    def update_publish_instance(
            self,
            instance_id: str,
            data: dict,
    ) -> None:
        """Update a publish instance in the current project.

        Args:
            instance_id (str): Publish instance id to update.
            data (dict): Data to update.

        """
        ayon_data = self.get_ayon_data()
        publish_instances = self.get_publish_instances()
        for idx, publish_instance in enumerate(publish_instances):
            if publish_instance["instance_id"] == instance_id:
                publish_instances[idx] = data
                break
        ayon_data[MOCHA_INSTANCES_KEY] = publish_instances

        self.update_ayon_data(ayon_data)

    def write_create_instances(
            self, instances: list[dict]) -> None:
        """Write publish instances to the current project."""
        ayon_data = self.get_ayon_data()
        ayon_data[MOCHA_INSTANCES_KEY] = instances
        self.update_ayon_data(ayon_data)

    def remove_create_instance(self, instance_id: str) -> None:
        """Remove a publishing instance from the current project.

        Args:
            instance_id (str): Publish instance id to remove.

        """
        data = self.get_ayon_data()
        publish_instances = self.get_publish_instances()
        publish_instances = [
            publish_instance
            for publish_instance in publish_instances
            if publish_instance["instance_id"] != instance_id
        ]
        data[MOCHA_INSTANCES_KEY] = publish_instances

        self.update_ayon_data(data)
