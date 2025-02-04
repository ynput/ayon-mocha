"""Settings for the Mocha Pro Addon."""
from ayon_server.settings import BaseSettingsModel, SettingsField

from .creator_plugins import MochaProCreatorPlugins


class MochaProSettings(BaseSettingsModel):
    """Settings for the Mocha Pro Addon."""
    create: MochaProCreatorPlugins = SettingsField(
        default_factory=MochaProCreatorPlugins,
        title="Creator Plugins")


DEFAULT_VALUES = {
    "create": {
        "CreateTrackingPoints": {
            "enabled": True,
            "default_exporters": [
                "Nuke7Tracker",
            ]
        },
        "CreateShapeData": {
            "enabled": True,
            "default_exporters": [
                "SilhouetteShapes",
            ]
        }
    }
}
