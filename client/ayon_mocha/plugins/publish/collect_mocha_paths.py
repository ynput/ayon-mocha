"""Collect Mocha executable paths."""
from __future__ import annotations

import platform
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pyblish.api
from mocha import get_mocha_exec_name

if TYPE_CHECKING:
    from logging import Logger

    from mocha.project import Project

class CollectMochaPaths(pyblish.api.ContextPlugin):
    """Collect Mocha Pro project."""
    order = pyblish.api.CollectorOrder - 0.45
    label = "Collect Mocha Pro executables"
    hosts: ClassVar[list[str]] = ["mochapro"]
    log: Logger

    def process(self, context: pyblish.api.Context) -> None:
        """Process the plugin."""
        project: Project = context.data["project"]
        self.log.info("Collected Mocha Pro project: %s", project)

        mocha_executable_path = Path(get_mocha_exec_name("mochapro"))
        context.data["mocha_executable_path"] = mocha_executable_path
        mocha_install_dir = mocha_executable_path.parent.parent

        if platform.system().lower() == "windows":
            mocha_python_path = (
                mocha_install_dir / "python" / "python.exe")
            mocha_exporter_path = (
                mocha_install_dir / "python" / "mochaexport.py")
        elif platform.system().lower() == "darwin":
            mocha_python_path = (
                mocha_install_dir / "python3")
            mocha_exporter_path = (
                mocha_install_dir / "mochaexport.py")
        elif platform.system().lower() == "linux":
            mocha_python_path = (
                mocha_install_dir / "python" / "bin" / "python3")
            mocha_exporter_path = (
                mocha_install_dir / "python" / "mochaexport.py")
        else:
            msg = f"Unsupported platform: {platform.system()}"
            raise NotImplementedError(msg)

        context.data["mocha_python_path"] = mocha_python_path
        context.data["mocha_exporter_path"] = mocha_exporter_path

        self.log.info("Collected Mocha Pro executable path: %s",
                      mocha_executable_path)
        self.log.info("Collected Mocha Pro python executable path: %s",
                      mocha_python_path)
        self.log.info("Collected Mocha Pro python export script path: %s",
                      mocha_exporter_path)
