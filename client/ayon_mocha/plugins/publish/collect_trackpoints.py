"""Collect instances for publishing."""
from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, ClassVar

import pyblish.api
from ayon_core.pipeline import KnownPublishError
from ayon_core.pipeline.create import get_product_name
from ayon_mocha.api.lib import get_exporters

if TYPE_CHECKING:
    from logging import Logger

    from ayon_core.pipeline.create import CreateContext
    from mocha.project import Layer, Project


class CollectTrackpoints(pyblish.api.InstancePlugin):
    """Collect trackpoint data."""
    label = "Collect Tracking Data"
    order = pyblish.api.CollectorOrder - 0.45
    hosts: ClassVar[list[str]] = ["mochapro"]
    families: ClassVar[list[str]] = ["trackpoints"]
    log: Logger


    @staticmethod
    def new_product_name(
        create_context: CreateContext,
        layer_name: str,
        product_type: str,
        variant: str) -> str:
        """Return the new product name."""
        sanitized_layer_name = layer_name.replace(" ", "_")
        variant = f"{sanitized_layer_name}{variant.capitalize()}"

        return get_product_name(
            project_name=create_context.project_name,
            task_name=create_context.get_current_task_name(),
            task_type=create_context.get_current_task_type(),
            host_name=create_context.host_name,
            product_type=product_type,
            variant=variant,
        )

    def process(self, instance: pyblish.api.Instance) -> None:
        """Process the instance."""
        # copy creator settings to the instance itself
        creator_attrs = instance.data["creator_attributes"]
        registered_exporters = get_exporters()
        selected_exporters = [
            exporter
            for exporter in registered_exporters
            if exporter.id in creator_attrs["exporter"]
        ]

        instance.data["use_exporters"] = selected_exporters
        instance.data["exporter_options"] = {
            "invert": creator_attrs["invert"],
            "frame_time": creator_attrs["frame_time"],
            "remove_lens_distortion": creator_attrs["remove_lens_distortion"],
        }

        project: Project = instance.context.data["project"]
        layers: list[Layer] = []
        if creator_attrs["layer_mode"] == "selected":
            layers.extend(
                project.layers[selected_layer_idx]
                for selected_layer_idx in creator_attrs["layers"]
            )
        elif creator_attrs["layer_mode"] == "all":
            layers = project.layers
        else:
            msg = f"Invalid layer mode: {creator_attrs['layer_mode']}"
            raise KnownPublishError(msg)

        for layer in layers:
            new_instance = instance.context.create_instance(
                f"{instance.name}_{layer.name}"
            )
            for k, v in instance.data.items():
                # this is needed because the data is not always
                # "deepcopyable".
                try:
                    new_instance.data[k] = deepcopy(v)
                except TypeError:  # noqa: PERF203
                    new_instance.data[k] = v

            # new_instance.data = instance.data
            new_instance.data["label"] = f"{instance.name} ({layer.name})"
            new_instance.data["name"] = f"{instance.name}_{layer.name}"
            new_instance.data["productName"] = self.new_product_name(
                instance.context.data["create_context"],
                layer.name,
                instance.data["productType"],
                instance.data["variant"],
            )
            self.set_layer_data_on_instance(new_instance, layer)

        instance.context.remove(instance)


    def set_layer_data_on_instance(
            self, instance: pyblish.api.Instance, layer: Layer) -> None:
        """Set data on instance."""
        instance.data["layer"] = layer
        instance.data["frameStart"] = layer.in_point()
        instance.data["frameEnd"] = layer.out_point()
