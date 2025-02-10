"""Validate layers and exportes."""
from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, ClassVar

import pyblish.api
from ayon_core.pipeline import PublishValidationError

if TYPE_CHECKING:
    from logging import Logger


class ValidateLayersAndExporters(pyblish.api.InstancePlugin):
    """Validate layers and exporters set."""

    order = pyblish.api.Validator.order + 0.1
    label = "Validate Exporters and Layers"
    hosts: ClassVar[list[str]] = ["mochapro"]
    families: ClassVar[list[str]] = ["matteshapes", "trackpoints"]
    log: Logger

    def process(self, instance: pyblish.api.Instance) -> None:
        """Process all the trackpoints.

        Raises:
            PublishValidationError: If no layers or exporters are set.

        """
        self.log.debug("Validating layers and exporters")
        if not instance.data.get("layer"):
            msg = (
                f"No layers set for instance {instance.name}"
            )
            raise PublishValidationError(
                msg, description=self._missing_layer_description())

        if not instance.data.get("use_exporters"):
            msg = (
                f"No exporters set for instance {instance.name}"
            )
            raise PublishValidationError(
                msg, description=self._missing_exporter())

    @classmethod
    def _missing_layer_description(cls) -> str:
        """Return the description for missing layer."""
        return inspect.cleandoc(
            """
            ### Issue

            The instance doesn't have layers set. Please select the layer
            in the publisher,or set the layer mode to "All layers".
            """
        )

    @classmethod
    def _missing_exporter(cls) -> str:
        """Return the description for missing layer."""
        return inspect.cleandoc(
            """
            ### Issue

            You need to select at least one exporter.
            """
        )
