"""BorisFX Mocha Pro addon for AYON."""
from __future__ import annotations

import os
from typing import Any

from ayon_core.addon import AYONAddon, IHostAddon

from .version import __version__

MOCHA_ADDON_ROOT = os.path.dirname(os.path.abspath(__file__))


class MochaAddon(AYONAddon, IHostAddon):
    """BorisFX Mocha Pro addon for AYON."""

    name = "mocha"
    host_name = "mochapro"
    title = "Mocha Pro"
    version = __version__

    @staticmethod
    def add_implementation_envs(env: dict[str, str], _app: Any) -> None:  # noqa: ANN401
        """Add implementation environment variables."""
        startup_path = os.path.join(MOCHA_ADDON_ROOT, "startup")
        env["MOCHA_INIT_SCRIPT"] = startup_path

    def get_workfile_extensions(self) -> list[str]:  # noqa: PLR6301
        """Return supported workfile extensions."""
        return [".mocha"]
