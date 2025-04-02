"""Load a clip from a file as trackable clip."""
from __future__ import annotations

import time
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Optional

from ayon_core.lib.transcoding import IMAGE_EXTENSIONS
from ayon_core.pipeline import get_representation_path, registered_host
from ayon_core.pipeline.load import LoadError
from ayon_mocha.api.lib import get_image_info, update_ui
from ayon_mocha.api.pipeline import (
    Container,
    MochaProHost,
)
from ayon_mocha.api.plugin import MochaLoader

if TYPE_CHECKING:
    from mocha.project import Clip


class LoadTrackableClip(MochaLoader):
    """Load a clip from a file."""

    label = "Load Trackable Clip"
    order = -11
    icon = "code-fork"
    color = "orange"

    product_types: ClassVar[set[str]] = {"*"}
    representations: ClassVar[set[str]] = {"*"}
    extensions: ClassVar[set[str]] = {
        ext.lstrip(".") for ext in IMAGE_EXTENSIONS}

    def load(self,
             context: dict,
             name: Optional[str] = None,
             namespace: Optional[str] = None,
             options: Optional[dict] = None) -> None:
        """Load a clip from a file as trackable clip.

        Raises:
            LoadError: If no trackable clip found in the project.

        """
        host: MochaProHost = registered_host()
        project = host.get_current_project()
        with project.undo_group():

            current_clip: Clip = project.default_trackable_clip
            if current_clip is None:
                msg = "No trackable clip found in the project."
                raise LoadError(msg)
            # no way how to change clip name
            # project.parameter([current_clip, "name"]).set(name)

            file_path = self.filepath_from_context(context)

            try:
                image_info = get_image_info(file_path)
            except ValueError as exc:
                msg = (
                    f"Failed to get image info from {file_path}: {exc}"
                )
                raise LoadError(msg) from exc

            # set clip properties
            current_clip.frame_size = (
                image_info.get("width", 1920),
                image_info.get("height", 1080)
            )

            current_clip.relink(file_path)

            for cnt in host.get_containers():
                if cnt.get("name") == current_clip.name:
                    cnt["representation"] = str(
                        context["representation"]["id"])
                    return

            container = Container(
                name=current_clip.name,
                namespace=namespace or "",
                loader=self.__class__.__name__,
                representation=str(context["representation"]["id"]),
                objectName=current_clip.name,
                timestamp=time.time_ns()
            )
            host.add_container(container)

    def switch(self, container: dict, context: dict) -> None:
        """Switch the image sequence on the current camera."""
        self.update(container, context)

    def remove(self, container: dict) -> None:
        """Remove a container."""
        host: MochaProHost = registered_host()
        project = host.get_current_project()

        clips = project.get_clips()
        clip = clips.get(container["objectName"])
        if not clip:
            self.log.warning("Clip %s not found", container["objectName"])
            return
        del clip
        host.remove_container(Container(**container))

    def update(self, container: dict, context: dict) -> None:
        """Update a container.

        Raises:
            LoadError: If the clip information cannot be determined.

        """
        host: MochaProHost = registered_host()

        version_entity = context["version"]
        repre_entity = context["representation"]

        file_path = get_representation_path(repre_entity)
        project = host.get_current_project()
        clips = project.get_clips()

        try:
            image_info = get_image_info(Path(file_path))
        except ValueError as exc:
            msg = f"Failed to get image info from {file_path}: {exc}"
            raise LoadError(msg) from exc
        try:
            clips[container["objectName"]].relink(file_path)
            # set clip properties
            clips[container["objectName"]].frame_size = (
                image_info.get("width", 1920),
                image_info.get("height", 1080),
            )
        except KeyError:
            self.log.warning("Clip %s not found", container["objectName"])
        update_ui()

        container["representation"] = repre_entity["id"]
        container["version"] = str(version_entity["version"])
        host.add_container(Container(**container))
