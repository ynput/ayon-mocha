"""Validate layer names in trackpoints."""
from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, ClassVar

import pyblish.api
from ayon_core.pipeline import PublishValidationError

if TYPE_CHECKING:
    from logging import Logger



class ValidateTrackpointLayers(pyblish.api.Validator):
    """Validate layer names in trackpoints."""

    order = pyblish.api.Validator.order + 0.1
    label = "Validate Trackpoint Layers"
    hosts: ClassVar[list[str]] = ["mochapro"]
    families: ClassVar[list[str]] = ["trackpoints"]
    log: Logger

    def process(self, instance: pyblish.api.Instance) -> None:
        """Process all the trackpoints."""
        if not instance.data.get("layer"):
            msg = (
                f"Specified layer index ({instance.data['layer']} "
                "does not exist in the project"
            )
            raise PublishValidationError(
                msg, description=self._missing_layer_description())

        if len(instance.data["use_exporters"]) == 0:
            msg = (
                "Multiple exporters are not supported for trackpoints. "
                "Please use only one exporter"
            )
            raise PublishValidationError(
                msg, description=self._missing_exporter())

    @classmethod
    def _missing_layer_description(cls) -> str:
        """Return the description for missing layer."""
        return inspect.cleandoc(
            """
            ### Issue

            The instance is missing the layer attribute. Select the layer
            in the publisher.
            """
        )

    @classmethod
    def _missing_exporter(cls) -> str:
        """Return the description for missing layer."""
        return inspect.cleandoc(
            """
            ### Issue

            You need to select at least one exporter on the instance.
            """
        )
