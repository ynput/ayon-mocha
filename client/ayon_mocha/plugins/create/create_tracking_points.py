"""Create tracking data instance."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ayon_core.lib import (
    BoolDef,
    EnumDef,
    NumberDef,
    UILabelDef,
    UISeparatorDef,
)
from ayon_mocha.api.lib import get_mocha_version, get_tracking_exporters
from ayon_mocha.api.plugin import MochaCreator

if TYPE_CHECKING:
    from ayon_core.pipeline import CreatedInstance



class CreateTrackingPoints(MochaCreator):
    """Create tracking points instance."""
    identifier = "io.ayon.creators.mochapro.trackpoints"
    label = "Track Points"
    description = __doc__
    product_type = "trackpoints"
    icon = "cubes"


    def get_attr_defs_for_instance(self, instance: CreatedInstance) -> list:
        """Get attribute definitions for instance."""
        version = get_mocha_version()
        settings = (
            self.project_settings
                ["mocha"]["create"]["CreateTrackingPoints"]
        )

        try:
            exporter_settings = (
                settings
                [f"mocha_{version}"]
                ["default_exporters"]
            )
        except KeyError:
            exporter_settings = (
                settings
                ["mocha_2024_5"]
                ["default_exporters"]
            )

        exporters = get_tracking_exporters()
        exporter_items = {ex.id: ex.label for ex in exporters}

        preselect_exporters =  [
            ex.id
            for ex in exporters
            if ex.short_name in exporter_settings
        ]

        layers = {
                    idx: layer.name
                    for idx, layer in enumerate(
                        self.create_context.host.get_current_project().layers)
                } or {-1: "No layers"}

        return [
            EnumDef("layers",
                    label="Layers",
                    items=layers,
                    multiselection=True),
            EnumDef("exporter",
                    label="Exporter format",
                    items=exporter_items,
                    multiselection=True,
                    default=preselect_exporters),
            UISeparatorDef(),
            UILabelDef(
                "Exporter Options (not all are available in all exporters)"),
            NumberDef(
                "frame_time", label="Frame time",
                default=0.0),
            BoolDef("invert", label="Invert", default=False),
            BoolDef("remove_lens_distortion",
                    label="Remove lens distortion", default=False),
            EnumDef("layer_mode", label="Layer mode",
                    items={
                        "selected": "Selected layers",
                        "all": "All layers"
                    }),

        ]


