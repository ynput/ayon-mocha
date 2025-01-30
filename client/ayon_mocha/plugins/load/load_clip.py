"""Load a clip from a file."""
from __future__ import annotations

import time
from typing import ClassVar, Optional

from ayon_core.lib.transcoding import IMAGE_EXTENSIONS
from ayon_core.pipeline import get_representation_path, registered_host
from ayon_mocha.api.lib import update_ui
from ayon_mocha.api.pipeline import (
    Container,
    MochaProHost,
)
from ayon_mocha.api.plugin import MochaLoader
from mocha.project import Clip


class LoadClip(MochaLoader):
    """Load a clip from a file."""

    label = "Load Clip"
    order = -10
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
        """Load a clip from a file."""
        host: MochaProHost = registered_host()
        project = host.get_current_project()
        with project.undo_group():
            file_path = self.filepath_from_context(context)
            clip = Clip(file_path, name)
            project.add_clip(clip, name)
            project.new_output_clip(clip, name)
            container = Container(
                name=name,
                namespace=namespace or "",
                loader=self.__class__.__name__,
                representation=str(context["representation"]["id"]),
                objectName=clip.name,
                timestamp=time.time_ns()
            )
            host.add_container(container)
            # This should show the clip in the UI, but it doesn't work
            # (mocha.ui.set_displayed_clip(clip))
            # https://borisfx.com/documentation/mocha/12.0.0/python-guide/#_obtaining_the_current_clip
            # set_displayed_clip(clip)
            update_ui()
            self.log.debug("Loaded clip: %s", clip)

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
        """Update a container."""
        host: MochaProHost = registered_host()

        version_entity = context["version"]
        repre_entity = context["representation"]

        file_path = get_representation_path(repre_entity)
        project = host.get_current_project()
        clips = project.get_clips()
        try:
            clips[container["objectName"]].relink(file_path)
        except KeyError:
            self.log.warning("Clip %s not found", container["objectName"])
        update_ui()

        container["representation"] = repre_entity["id"]
        container["version"] = str(version_entity["version"])
        host.add_container(Container(**container))

