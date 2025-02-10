"""Collect instances for publishing."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

import pyblish.api

if TYPE_CHECKING:
    from logging import Logger


class CollectInstances(pyblish.api.InstancePlugin):
    """Collect instances for publishing."""
    label = "Collect Instances"
    order = pyblish.api.CollectorOrder - 0.4
    hosts: ClassVar[list[str]] = ["mochapro"]
    log: Logger

    def process(self, instance: pyblish.api.Instance) -> None:
        """Process the plugin."""
        self.log.debug("Collecting data for %s", instance)

        # Define nice instance label
        instance_node = instance.data.get(
            "transientData", {}).get("instance_node")
        name = instance_node.label if instance_node else instance.name
        label = f"{name} ({instance.data['folderPath']})"

        # Set frame start handle and frame end handle if frame ranges are
        # available
        if "frameStart" in instance.data and "frameEnd" in instance.data:
            # Enforce existence if handles
            instance.data.setdefault("handleStart", 0)
            instance.data.setdefault("handleEnd", 0)

            # Compute frame start handle and end start handle
            frame_start_handle = (
                instance.data["frameStart"] - instance.data["handleStart"]
            )
            frame_end_handle = (
                instance.data["frameEnd"] - instance.data["handleEnd"]
            )
            instance.data["frameStartHandle"] = frame_start_handle
            instance.data["frameEndHandle"] = frame_end_handle

            # Include frame range in label
            label += f"  [{int(frame_start_handle)}-{int(frame_end_handle)}]"

        instance.data["label"] = label
