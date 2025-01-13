"""Server addon implementation."""
from __future__ import annotations

from typing import Type

from ayon_server.addons import BaseServerAddon

from .settings import DEFAULT_VALUES, MochaSettings


class MochaAddon(BaseServerAddon):
    """BorisFX Mocha Pro addon for AYON settings."""
    settings_model: Type[MochaSettings] = MochaSettings

    async def get_default_settings(self) -> dict:
        """Return default settings."""
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_VALUES)
