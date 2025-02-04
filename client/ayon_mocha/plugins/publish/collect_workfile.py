"""Collect the current working file."""
from __future__ import annotations

import os
from typing import ClassVar

import pyblish.api


class CollectWorkfileData(pyblish.api.InstancePlugin):
    """Collect Mocha workfile data."""

    order = pyblish.api.CollectorOrder - 0.01
    label = "Mocha Workfile"
    families: ClassVar[list[str]] = ["workfile"]

    def process(self, instance: pyblish.api.Instance) -> None:
        """Inject the current working file."""
        context = instance.context
        current_file = instance.context.data["currentFile"]
        folder, file = os.path.split(current_file)
        filename, ext = os.path.splitext(file)

        data = {
            "setMembers": [current_file],
            "frameStart": context.data["frameStart"],
            "frameEnd": context.data["frameEnd"],
            "handleStart": context.data["handleStart"],
            "handleEnd": context.data["handleEnd"],
            "representations": [{
                "name": ext.lstrip("."),
                "ext": ext.lstrip("."),
                "files": file,
                "stagingDir": folder,
            }]}

        instance.data.update(data)
